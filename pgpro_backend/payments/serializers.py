from rest_framework import serializers
from .models import Payment, PaymentTransaction

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'
        read_only_fields = ['id', 'paid_at']

class PaymentSerializer(serializers.ModelSerializer):
    transactions = PaymentTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'amount_paid',
                           'balance_due', 'status', 'late_fee']

class CollectPaymentSerializer(serializers.Serializer):
    tenant_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_month = serializers.DateField()
    payment_mode = serializers.ChoiceField(choices=[
        'upi', 'cash', 'bank_transfer', 'razorpay'
    ])
    transaction_ref = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)