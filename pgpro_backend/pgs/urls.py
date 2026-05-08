from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, RoomViewSet, BedViewSet

router = DefaultRouter()
router.register('properties', PropertyViewSet, basename='property')
router.register('rooms', RoomViewSet, basename='room')
router.register('beds', BedViewSet, basename='bed')

urlpatterns = [
    path('', include(router.urls)),
]