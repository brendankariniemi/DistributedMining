import logging
from django.core.management.base import BaseCommand
from mining.models import Pool
from mining.tasks import process_pool_task


class Command(BaseCommand):

    def handle(self, *args, **options):
        logging.info("Starting tasks for all active pools...")
        for pool in Pool.objects.all():
            process_pool_task(pool_id=pool.pool_id)
        logging.info('Successfully scheduled tasks!')
