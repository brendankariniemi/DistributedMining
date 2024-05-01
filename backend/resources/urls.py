from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CryptocurrencyViewSet, GuideViewSet, TutorialViewSet

router = DefaultRouter()
router.register(r'cryptocurrencies', CryptocurrencyViewSet)
router.register(r'guides', GuideViewSet)
router.register(r'tutorials', TutorialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
