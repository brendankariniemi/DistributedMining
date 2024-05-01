import logging
import os
import shutil
from paramiko import SSHClient, AutoAddPolicy
from django.core.management.base import BaseCommand
from mining.models import Hardware
from django.db import transaction


def create_client(hardware):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(hardware.ip_address, key_filename='/home/ubuntu/CSCI414.pem')

    local_path = f'./media/client_package/{hardware.pk}'
    remote_path = f'{hardware.client_path}/MiningClient'

    try:
        # Ensure the remote directory exists, create it if not
        mkdir_command = f"mkdir -p {remote_path}"
        stdin, stdout, stderr = client.exec_command(mkdir_command)
        stdout.channel.recv_exit_status()  # Wait for the command to complete
        if stderr.read():
            logging.error(f"Error creating remote directory: {stderr.read().decode()}")

        # Use SFTP to transfer directory contents
        sftp = client.open_sftp()
        try:
            # Walk through the local directory to replicate the directory structure and copy files
            for dirpath, dirnames, filenames in os.walk(local_path):
                remote_dirpath = dirpath.replace(local_path, remote_path)
                try:
                    sftp.stat(remote_dirpath)
                except IOError:
                    sftp.mkdir(remote_dirpath)  # Create remote directory if it does not exist

                for filename in filenames:
                    local_file = os.path.join(dirpath, filename)
                    remote_file = os.path.join(remote_dirpath, filename)
                    sftp.put(local_file, remote_file)
        finally:
            sftp.close()

        setup_venv = f"{hardware.python_path} -m venv {remote_path}/.venv"
        activate_venv = f"source {remote_path}/.venv/bin/activate"
        install_requirements = f"pip install --no-input -r {remote_path}/requirements.txt"
        command = f"{setup_venv} && {activate_venv} && {install_requirements}"

        # Execute the combined command
        stdin, stdout, stderr = client.exec_command(command)
        stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            logging.info(output)
        if error:
            logging.error(error)

        # Update the python_path in the Hardware model to the new virtual environment
        new_python_path = f"{remote_path}/.venv/bin/python"
        with transaction.atomic():
            hardware.python_path = new_python_path
            hardware.client_path = remote_path
            hardware.save()

        logging.info(f"Client created and Python path updated for hardware ID {hardware.hardware_id}")

    except Exception as e:
        logging.error(f"Failed to create client {hardware.hardware_id} at {hardware.ip_address}: {e}")
    finally:
        # Delete the local directory after copying everything over
        try:
            shutil.rmtree(local_path)
            logging.info(f"Successfully deleted local directory: {local_path}")
        except Exception as e:
            logging.error(f"Failed to delete local directory {local_path}: {e}")
        client.close()


def start_client(hardware):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        client.connect(hardware.ip_address, key_filename='/home/ubuntu/CSCI414.pem')
        command = f"nohup {hardware.python_path} {hardware.client_path}/mining-client.py > /dev/null 2>&1 &"
        stdin, stdout, stderr = client.exec_command(command)
        stdin.close()
        stderr.read()
        stdout.read()
        logging.info(f"Started client {hardware.hardware_id} at {hardware.ip_address}: STDOUT: {stdout.read()}, STDERR: {stderr.read()}")
    except Exception as e:
        logging.error(f"Failed to start client {hardware.hardware_id} at {hardware.ip_address}: {e}")
    finally:
        client.close()


class Command(BaseCommand):
    help = 'Starts Python client scripts on remote machines.'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        try:
            logging.info("Starting clients....")
            for hardware in Hardware.objects.all():
                start_client(hardware)
            logging.info('Successfully started clients!')
        except Exception as e:
            logging.error(f"An error occurred: {e}")

