import logging
from django.db.models import Sum, Count, Case, When, IntegerField
from rest_framework import viewsets
from rest_framework.response import Response
from mining.models import Pool
from mining.serializers import PoolSerializer

logger = logging.getLogger(__name__)


class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer

    def list(self, request, *args, **kwargs):
        # Fetch all pools with annotations for total earnings from solved blocks and hardware count
        queryset = Pool.objects.annotate(
            total_earnings=Sum(
                Case(
                    When(block__is_solved=True, then='block__reward_amount'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            hardware_count=Count('hardware', distinct=True)
        ).prefetch_related('cryptocurrency')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

