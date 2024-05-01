from django.contrib.auth.models import User
from rest_framework import serializers
from resources.serializers import CryptocurrencySerializer
from .models import Pool, Hardware, Block, Reward


class PoolSerializer(serializers.ModelSerializer):
    cryptocurrency = CryptocurrencySerializer(read_only=True)
    total_earnings = serializers.DecimalField(max_digits=18, decimal_places=8, read_only=True)
    hardware_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Pool
        fields = ['pool_id', 'creation_timestamp', 'cryptocurrency', 'total_earnings', 'hardware_count']


class HardwareSerializer(serializers.ModelSerializer):
    pool = serializers.PrimaryKeyRelatedField(queryset=Pool.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Hardware
        fields = ['pool', 'user', 'ip_address', 'hash_rate', 'python_path', 'client_path']

    def create(self, validated_data):
        hardware = Hardware.objects.create(**validated_data)
        return hardware


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

