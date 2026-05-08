from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Tenant
from .serializers import TenantSerializer
from .services import assign_tenant

class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tenant.objects.filter(
            property__owner=self.request.user
        ).select_related('room', 'bed', 'property')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tenant = assign_tenant(serializer.validated_data)
        
        return Response(
            TenantSerializer(tenant).data,
            status=status.HTTP_201_CREATED
        )