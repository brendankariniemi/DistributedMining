from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mining.views.pool_views import PoolViewSet
from mining.views.hardware_views import HardwareViewSet
from mining.views.reward_views import RewardViewSet


router = DefaultRouter()
router.register(r'pools', PoolViewSet)
router.register(r'hardware', HardwareViewSet)
router.register(r'rewards', RewardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]