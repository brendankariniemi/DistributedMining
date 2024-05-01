from django.db import models
from django.contrib.auth.models import User
from resources.models import Cryptocurrency


class Pool(models.Model):
    pool_id = models.AutoField(primary_key=True)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    creation_timestamp = models.DateTimeField()


class Hardware(models.Model):
    hardware_id = models.AutoField(primary_key=True)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash_rate = models.DecimalField(max_digits=18, decimal_places=8)
    ip_address = models.CharField(max_length=255)
    python_path = models.CharField(max_length=255)
    client_path = models.CharField(max_length=255)


class Block(models.Model):
    block_id = models.AutoField(primary_key=True)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    block_number = models.IntegerField(default=0)
    block_nonce = models.IntegerField(default=0)
    block_hash = models.CharField(max_length=255)
    mined_timestamp = models.DateTimeField()
    reward_amount = models.DecimalField(max_digits=18, decimal_places=8)
    is_solved = models.BooleanField(default=False)


class Reward(models.Model):
    reward_id = models.AutoField(primary_key=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    timestamp = models.DateTimeField()
