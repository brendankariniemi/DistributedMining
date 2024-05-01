import logging
from paramiko import SSHClient, AutoAddPolicy
from django.core.management.base import BaseCommand
from mining.models import Hardware


def kill_client(hardware):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        client.connect(hardware.ip_address, key_filename='/home/ubuntu/CSCI414.pem')
        # Command to read PID from config file
        read_pid_command = f"cat {hardware.client_path}/config.ini | grep client_pid | cut -d '=' -f2"
        stdin, stdout, stderr = client.exec_command(read_pid_command)
        pid = stdout.read().strip().decode()
        if pid:
            # Command to kill the process
            kill_command = f"kill {pid}"
            stdin, stdout, stderr = client.exec_command(kill_command)
            # Update the PID in the config file to -1 after killing the process
            update_pid_command = f"{hardware.python_path} {hardware.client_path}/mining-client.py --write-config client_pid=-1"
            stdin, stdout, stderr = client.exec_command(update_pid_command)
            logging.info(f"Killed client {hardware.hardware_id} at {hardware.ip_address} with PID: {pid} and updated PID to -1")
        else:
            logging.warning(f"No PID found for client {hardware.hardware_id} at {hardware.ip_address}.")
    except Exception as e:
        logging.error(f"Failed to kill client {hardware.hardware_id} at {hardware.ip_address}: {e}")
    finally:
        client.close()


class Command(BaseCommand):
    help = 'Kills all running Python client scripts on remote machines.'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        try:
            logging.info("Killing clients....")
            for hardware in Hardware.objects.all():
                kill_client(hardware)
            logging.info('Successfully killed all clients!')
        except Exception as e:
            logging.error(f"An error occurred: {e}")

