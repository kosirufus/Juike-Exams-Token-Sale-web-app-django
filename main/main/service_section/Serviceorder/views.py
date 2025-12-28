from click import group
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
import requests

from .models import ServiceOrder
from service_section.Whatsappgroup.models import WhatsAppAccessToken, WhatsappGroup


@api_view(['GET'])
def order_success(request, reference):
    try:
        order = ServiceOrder.objects.get(reference=reference)
    except ServiceOrder.DoesNotExist:
        return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Verify payment with Paystack
    verify_url = f"https://api.paystack.co/transaction/verify/{order.reference}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    paystack_resp = requests.get(verify_url, headers=headers, timeout=30).json()

    if not (paystack_resp.get("status") and paystack_resp.get("data", {}).get("status") == "success"):
        return Response({"detail": "Payment not completed or failed"}, status=status.HTTP_400_BAD_REQUEST)

    if not order.is_paid:
        order.is_paid = True
        order.save()

    # Create one token per order (no group here)
    token_obj = WhatsAppAccessToken.objects.create(order=order)

    # Fetch active WhatsApp groups for this order
    groups = WhatsappGroup.objects.filter(
        product__in=order.products.all(),
        student_class=order.student_class,
        is_active=True
    )

    group_data = [{"id": g.id, "product_name": g.product.name} for g in groups]

    return Response({
        "full_name": order.full_name,
        "products": [p.name for p in order.products.all()],
        "whatsapp_button_token": str(token_obj.token),
        "groups": group_data
    })


# Serviceorder/views.py
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from service_section.Whatsappgroup.models import WhatsAppAccessToken, WhatsappGroup

import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def redirect_to_whatsapp(request, token):
    """
    Redirects user to a WhatsApp group link using a one-time token.
    """

    # Fetch the token object or 404
    token_obj = get_object_or_404(WhatsAppAccessToken, token=token)
    logger.info(f"[WhatsApp Redirect] Fetched token: {token_obj.token} for order {token_obj.order.reference}")

    # Check if token is expired
    if token_obj.is_expired():
        logger.warning(f"[WhatsApp Redirect] Token expired: {token_obj.token}")
        return Response({"detail": "Link expired"}, status=status.HTTP_403_FORBIDDEN)

    # Get group ID from query params
    group_id = request.GET.get("group")
    if not group_id:
        logger.warning(f"[WhatsApp Redirect] No group specified for token: {token_obj.token}")
        return Response({"detail": "Group not specified"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the group, must match product(s) and student_class in order
    group = WhatsappGroup.objects.filter(
        id=group_id,
        product__in=token_obj.order.products.all(),
        student_class=token_obj.order.student_class,
        is_active=True
    ).first()

    if not group:
        logger.warning(f"[WhatsApp Redirect] Invalid group {group_id} for token: {token_obj.token}")
        return Response({"detail": "Invalid group"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if group already joined
    if token_obj.joined_groups.filter(id=group.id).exists():
        logger.info(f"[WhatsApp Redirect] Group {group.id} already joined by token {token_obj.token}")
        return Response({"detail": "Group already joined"}, status=status.HTTP_409_CONFLICT)

    # Add group to joined_groups
    token_obj.joined_groups.add(group)
    logger.info(f"[WhatsApp Redirect] Group {group.id} added to token {token_obj.token}")
    logger.info(f"[WhatsApp Redirect] Current joined groups: {list(token_obj.joined_groups.values_list('id', flat=True))}")

    # If all groups joined, expire token
    allowed_groups_count = WhatsappGroup.objects.filter(
        product__in=token_obj.order.products.all(),
        student_class=token_obj.order.student_class,
        is_active=True
    ).count()

    if token_obj.joined_groups.count() >= allowed_groups_count:
        token_obj.expires_at = timezone.now()
        token_obj.save()
        logger.info(f"[WhatsApp Redirect] Token {token_obj.token} expired after joining all groups")

    # Redirect to the real WhatsApp group link
    logger.info(f"[WhatsApp Redirect] Redirecting token {token_obj.token} to group link: {group.group_link}")
    return Response({"url": group.group_link})
