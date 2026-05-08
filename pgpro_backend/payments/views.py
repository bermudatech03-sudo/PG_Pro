from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer, CollectPaymentSerializer
from .services import collect_payment

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        return Payment.objects.filter(
            property__owner=self.request.user
        ).select_related('tenant', 'property').prefetch_related('transactions')

    @action(detail=False, methods=['post'], url_path='collect')
    def collect(self, request):
        serializer = CollectPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = collect_payment(**serializer.validated_data)

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='unpaid')
    def unpaid(self, request):
        unpaid = Payment.objects.filter(
            property__owner=request.user,
            status__in=['pending', 'partial', 'overdue']
        ).select_related('tenant', 'property')

        return Response(
            PaymentSerializer(unpaid, many=True).data
        )