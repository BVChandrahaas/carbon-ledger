from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmissionFactorViewSet

router = DefaultRouter()
router.register(r'', EmissionFactorViewSet, basename='emission-factor')

urlpatterns = [
    path('', include(router.urls)),
]
