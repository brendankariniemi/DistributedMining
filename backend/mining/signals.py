import shutil
import subprocess
from datetime import datetime
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from mining.models import Hardware, Block, Reward
from mining.management.commands.start_clients import create_client, start_client
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Hardware)
def handle_new_hardware(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New hardware added with ID: {instance.pk}")

        # Define paths
        template_path = './media/client_package/'
        new_client_path = f'./media/client_package/{instance.pk}'

        # Step 1: Create client directory from template
        try:
            shutil.copytree(template_path, new_client_path)
            logger.info("Successfully copied client package.")
        except Exception as e:
            logger.error(f"Failed to copy client package: {e}")
            return

        # Step 2: Run the Python script to personalize the config to the client
        config_script = f"python {new_client_path}/mining-client.py --write-config hardware_id={instance.hardware_id}"
        try:
            subprocess.run(config_script, check=True, shell=True)
            logger.info("Successfully wrote client configuration.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running config script: {e}")
            return

        # Step 3: Call create and deploy client
        try:
            create_client(instance)
            start_client(instance)
        except Exception as e:
            logger.error(f"Failed to execute management commands: {e}")


@receiver(post_save, sender=Block)
def handle_block_solved(sender, instance, created, **kwargs):
    if instance.is_solved:
        pool_hash_rate = Hardware.objects.filter(pool=instance.pool_id).aggregate(Sum('hash_rate'))['hash_rate__sum'] or 0
        hardware_records = Hardware.objects.filter(pool=instance.pool_id)

        if pool_hash_rate > 0:
            rewards = []
            for hardware in hardware_records:
                reward_amount = (hardware.hash_rate / pool_hash_rate) * instance.reward_amount
                reward = Reward(
                    block=instance,
                    hardware=hardware,
                    amount=reward_amount,
                    timestamp=datetime.now(),
                )
                logger.info(
                    f"New rewards created for block: {reward.block}, hardware: {reward.hardware}, and amount: {reward.amount}")
                rewards.append(reward)
            Reward.objects.bulk_create(rewards)
        else:
            logger.debug("No hash rate found for pool.")

