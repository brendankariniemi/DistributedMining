import random
import hashlib
import logging
from datetime import datetime
from decimal import Decimal
from background_task import background
from .models import Block, Pool

logger = logging.getLogger(__name__)


@background(schedule=1)
def process_pool_task(pool_id):
    try:
        pool = Pool.objects.get(pool_id=pool_id)
        last_block = Block.objects.filter(pool=pool).order_by('-block_number').first()
        block_number = last_block.block_number + 1 if last_block else 1

        if last_block and not last_block.is_solved:
            logger.info(f"Continuing to work on existing unsolved block: {last_block.block_hash}")
            return

        nonce = random.randint(0, 1000000)
        block_data = f"{block_number}{last_block.block_hash if last_block else '0' * 64}{nonce}"
        block_hash = hashlib.sha256(block_data.encode()).hexdigest()
        random_reward_amount = Decimal(random.random() * 100).quantize(Decimal('.01'))

        new_block = Block.objects.create(
            pool=pool,
            block_number=block_number,
            block_nonce=0,
            block_hash=block_hash,
            mined_timestamp=datetime.now(),
            reward_amount=random_reward_amount,
            is_solved=False
        )
        logger.info(f"New block created for pool {pool_id} with block number {block_number}, hash: {new_block.block_hash}, and reward amount: {new_block.reward_amount}")

    except Exception as e:
        logger.error(f'Error in process_pool_task for pool {pool_id}: {str(e)}')
    finally:
        process_pool_task(schedule=60, pool_id=pool_id)
