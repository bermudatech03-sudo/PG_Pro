from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from .models import Payment, PaymentTransaction
from tenants.models import Tenant

def get_or_create_monthly_payment(tenant, payment_month):
    payment, created = Payment.objects.get_or_create(
        tenant=tenant,
        payment_month=payment_month,
        defaults={
            'property': tenant.property,
            'amount_due': tenant.rent_amount,
            'amount_paid': 0,
            'late_fee': 0,
            'discount': 0,
            'balance_due': tenant.rent_amount,
            'due_date': payment_month.replace(day=tenant.rent_due_day),
            'status': 'pending'
        }
    )
    return payment

def collect_payment(tenant_id, amount, payment_month, payment_mode, transaction_ref=None, notes=None):
    try:
        tenant = Tenant.objects.get(id=tenant_id)
    except Tenant.DoesNotExist:
        raise ValidationError("Tenant not found.")

    if amount <= 0:
        raise ValidationError("Payment amount must be greater than zero.")

    payment = get_or_create_monthly_payment(tenant, payment_month)

    if payment.status == 'paid':
        raise ValidationError("Rent for this month is already fully paid.")

    with transaction.atomic():
        # Create transaction record
        PaymentTransaction.objects.create(
            payment=payment,
            tenant=tenant,
            amount=amount,
            payment_mode=payment_mode,
            transaction_ref=transaction_ref,
            notes=notes
        )

        # Update payment record
        payment.amount_paid += amount
        payment.balance_due = payment.amount_due + payment.late_fee - payment.amount_paid - payment.discount

        # Update status
        if payment.balance_due <= 0:
            payment.status = 'paid'
            payment.balance_due = 0
        elif payment.amount_paid > 0:
            payment.status = 'partial'

        payment.save()

    return payment


def apply_late_fee(payment_id, late_fee_amount):
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        raise ValidationError("Payment not found.")

    with transaction.atomic():
        payment.late_fee = late_fee_amount
        payment.balance_due = payment.amount_due + payment.late_fee - payment.amount_paid - payment.discount
        if payment.status != 'paid':
            payment.status = 'overdue'
        payment.save()

    return payment