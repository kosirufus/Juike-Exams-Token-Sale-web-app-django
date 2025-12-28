from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from tokens.models import Product, Token
from .models import Order, AssignedToken
import requests
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

# 1️⃣ Create Paystack session
@csrf_exempt
@api_view(['POST'])
def create_paystack_session(request):
    data = request.data
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1)) # converts quantity to integer that mathematical operation ca be performed on

    # Get product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    # Optional: check token availability
    available = Token.objects.filter(product=product, assigned=False).count()
    if quantity > available:
        return Response(
            {"error": "Quantity exceeds available tokens."},
            status=400
        )

    # 3️⃣ Create the order in DB FIRST
    order = Order.objects.create(
        product=product,
        quantity=quantity,
        amount=Decimal(product.price) * quantity
    )

    # 4️⃣ Prepare payload for Paystack
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "email": request.user.email if request.user.is_authenticated else "test@example.com",
        "amount": int(order.amount * 100),  # convert Naira to kobo
        "reference": str(order.reference),  # 🔥 This is the key fix
        "callback_url": "http://localhost:3000/payment-success",
        "metadata": {
            "service_type": "exam_token",
            "order_id": order.id
            } # for webhook
    }

    # Initialize payment
    try:
        res = requests.post(
            "https://api.paystack.co/transaction/initialize",
            json=payload,
            headers=headers
        )
        res.raise_for_status()
        data = res.json()
    except requests.exceptions.RequestException as e:
        return Response({"error": "Payment initiation failed", "details": str(e)}, status=500)

    # Return both authorization_url and reference to frontend
    return Response({
        "authorization_url": data["data"]["authorization_url"],
        "reference": str(order.reference)
    })

   
@api_view(['GET'])
def verify_paystack(request):
    reference = request.GET.get("reference")
    
    try:
        order = Order.objects.get(reference=reference)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    res = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers=headers
    ).json()

    if res["data"]["status"] == "success":
        return Response({
            "message": "Payment verified",
            "reference": reference
        })

    return Response({"error": "Payment not successful"}, status=400)

@api_view(['GET'])
def assigned_tokens(request):
    reference = request.GET.get('reference', '').strip()

    tokens = AssignedToken.objects.filter(order__reference=reference)

    data = [{
        "id": t.id,
        "code": t.token.code,
        "product_name": t.token.product.name,
        "product_session": t.token.product.session
    } for t in tokens]

    return Response(data)
