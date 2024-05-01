import logging
from django.db.models import Sum, F, Window
from rest_framework import viewsets
from rest_framework.response import Response
from mining.models import Reward
from mining.serializers import RewardSerializer

logger = logging.getLogger(__name__)


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    def get_queryset(self):
        # Filter for logged in user
        return Reward.objects.filter(hardware__user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Aggregate rewards per hardware
        rewards_per_hardware = queryset.values('hardware_id').annotate(
            total_rewards=Sum('amount')
        ).order_by('hardware_id')

        # Prepare data for cumulative rewards graph
        cumulative_data = queryset.annotate(
            cumulative_rewards=Window(
                expression=Sum('amount'),
                order_by=F('timestamp').asc()
            )
        ).values('timestamp', 'cumulative_rewards').distinct().order_by('timestamp')

        # Combine the data into a single response
        data = {
            'rewards_per_hardware': list(rewards_per_hardware),
            'cumulative_rewards': list(cumulative_data),
        }
        return Response(data)
