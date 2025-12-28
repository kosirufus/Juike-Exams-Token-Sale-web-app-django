# service_section/Payment/handlers.py
from django.db import transaction
from service_section.Serviceorder.models import ServiceOrder
from service_section.Payment.models import Payment


def handle_service_payment(event):
    data = event['data']
    metadata = data.get('metadata', {})

    reference = data['reference']
    paid_amount = data['amount'] / 100  # Kobo → Naira

    try:
        order = ServiceOrder.objects.get(reference=reference)
    except ServiceOrder.DoesNotExist:
        raise ValueError("Service order not found")

    # Idempotency
    if Payment.objects.filter(paystack_reference=reference).exists():
        return

    # Amount verification
    if paid_amount != float(order.amount):
        raise ValueError("Amount mismatch")

    # Atomic fulfillment
    with transaction.atomic():
        order.is_paid = True
        order.save()

        Payment.objects.create(
            order=order,
            paystack_reference=reference,
            amount=paid_amount,
            status='success'
        )
