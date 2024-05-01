import os
import signal
import subprocess
import atexit
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Starts the Django server and the background task processing.'

    def handle(self, *args, **options):
        background_processes = []

        def cleanup_processes():
            print("Cleaning up background processes...")
            for p in background_processes:
                if p.poll() is None:
                    p.terminate()
                    p.wait()
            print("Background processes terminated.")

        atexit.register(cleanup_processes)

        if os.environ.get('RUN_MAIN') == 'true':
            signal.signal(signal.SIGINT, lambda signum, frame: exit(0))
            signal.signal(signal.SIGTERM, lambda signum, frame: exit(0))

            background_processes.extend([
                subprocess.Popen(['python', 'manage.py', 'process_tasks']),
                subprocess.Popen(['python', 'manage.py', 'start_background']),
                subprocess.Popen(['python', 'manage.py', 'start_clients'])
            ])

        else:
            print("Not starting background processes due to auto-reloader.")

        # Run the server in the main thread
        try:
            call_command('runserver', '0.0.0.0:8000')
        finally:
            cleanup_processes()
            call_command('stop_clients')

