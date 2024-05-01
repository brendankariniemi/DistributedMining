import logging
from datetime import datetime
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from mining.models import Hardware, Reward, Block
from mining.serializers import HardwareSerializer

logger = logging.getLogger(__name__)


class HardwareViewSet(viewsets.ModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Hardware registered successfully.", "data": serializer.data},
                            status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='get-task')
    def get_task(self, request):
        # Retrieve hardware ID from query parameters
        hardware_id = request.query_params.get('hardware_id')
        if not hardware_id:
            return Response({'message': 'Hardware ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hardware = Hardware.objects.get(pk=hardware_id)
        except Hardware.DoesNotExist:
            return Response({'message': 'Hardware not found'}, status=status.HTTP_404_NOT_FOUND)

        task = self.assign_task_to_hardware(hardware)
        if task:
            return Response(task, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No task available for this hardware.'}, status=status.HTTP_200_OK)

    def assign_task_to_hardware(self, hardware):
        unsolved_block = Block.objects.filter(pool=hardware.pool, is_solved=False).first()
        if unsolved_block:
            nonce_range = self.calculate_nonce_range(hardware)
            return {
                'block_id': unsolved_block.block_id,
                'block_number': unsolved_block.block_number,
                'previous_hash': unsolved_block.block_hash,
                'nonce_range': nonce_range
            }
        return None

    def calculate_nonce_range(self, hardware):
        base_nonce = 0
        range_size = int(hardware.hash_rate * 100)
        return base_nonce, base_nonce + range_size

    @action(detail=False, methods=['post'], url_path='submit-result')
    def submit_result(self, request):
        result_data = request.data
        block_id = result_data.get('block_id')

        if not block_id:
            logger.error('Block ID not provided.')
            return Response({'error': 'Block ID must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            block = Block.objects.get(pk=block_id)
        except Block.DoesNotExist:
            logger.error('Block with ID {} not found.'.format(block_id))
            return Response({'error': 'Block not found.'}, status=status.HTTP_404_NOT_FOUND)

        if self.validate_block_solution(result_data):
            block.is_solved = True
            block.block_nonce = result_data['nonce']
            block.block_hash = result_data['hash']
            block.save()
            logger.info('Block with ID {} solved successfully.'.format(block_id))
            return Response({'message': 'Block solved successfully'}, status=status.HTTP_200_OK)
        else:
            logger.error('Invalid solution submitted for block ID {}.'.format(block_id))
            return Response({'error': 'Solution not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def validate_block_solution(self, result):
        return result['hash'].startswith('0000')

