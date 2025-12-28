from django.db import transaction
from .models import Order, AssignedToken, Token

def handle_exam_token_payment(event):
    """
    Event is the payload from Paystack webhook.
    Assigns tokens and marks order as paid.
    """
    data = event['data']
    metadata = data.get('metadata', {})
    order_id = metadata.get('order_id')
    reference = data['reference']

    # Get the order
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise ValueError(f"Order {order_id} not found")

    # Idempotency: skip if already processed
    if order.status.upper() == "PAID":
        return

    # Mark order as paid
    with transaction.atomic():
        order.status = "PAID"
        order.save()

        # Assign tokens
        tokens = Token.objects.filter(product=order.product, assigned=False)[:order.quantity]
        if len(tokens) < order.quantity:
            raise ValueError("Not enough unassigned tokens")

        for token in tokens:
            AssignedToken.objects.create(order=order, token=token)
            token.assigned = True
            token.save()
