from rest_framework import viewsets, permissions
from .models import Property, Room, Bed
from .serializers import PropertySerializer, RoomSerializer, BedSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(
            owner=self.request.user
        ).prefetch_related('rooms__beds')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(
            property__owner=self.request.user
        ).prefetch_related('beds')

class BedViewSet(viewsets.ModelViewSet):
    serializer_class = BedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bed.objects.filter(
            room__property__owner=self.request.user
        )