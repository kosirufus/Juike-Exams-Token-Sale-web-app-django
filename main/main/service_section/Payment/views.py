import uuid
import requests
from decimal import Decimal
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from service_section.Serviceorder.models import ServiceOrder
from service_section.Serviceproduct.models import ServiceProduct
from service_section.Subject.models import Subject
from service_section.Serviceorder.serializers import ServiceOrderCreateSerializer




@api_view(['POST'])
def create_payment(request):
    print("Incoming request.data:", request.data)

    try:
        serializer = ServiceOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    except Exception as e:
        print("Serializer validation failed:", e)
        return Response({"error": "Validation failed", "details": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    print("Serializer validated data:", data)


    reference = str(uuid.uuid4())

    # Fetch products
    products = ServiceProduct.objects.filter(id__in=data['product_ids'])
    amount = sum((product.price for product in products), Decimal('0.00'))

    # Create order
    order = ServiceOrder.objects.create(
        full_name=data['full_name'],
        email=data['email'],
        student_class=data['student_class'],
        amount=amount,
        reference=reference
    )
    order.products.set(products)

    # Fetch subjects
    subjects = Subject.objects.filter(id__in=data['subject_ids'])
    order.subjects.set(subjects)

    # Initialize Paystack transaction
    try:
        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            headers={
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                "email": order.email,
                "amount": int(order.amount * 100),  # Kobo
                "reference": order.reference,
                "callback_url": f"{settings.FRONTEND_URL}/servicesuccess",
                "metadata": {
                    "service_type": "service_booking",
                    "order_id": 123
                    }
            },
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        print("RequestException:", e)
        return Response(
            {"error": "Failed to contact Paystack", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Debug: print HTTP status and raw response
    print("HTTP status code:", response.status_code)
    print("Raw response text:", response.text)

    # Parse JSON safely
    try:
        paystack_response = response.json()
        print("Paystack response JSON:", paystack_response)
    except Exception as e:
        print("Failed to parse Paystack JSON:", e)
        return Response(
            {"error": "Invalid response from Paystack", "details": response.text},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Check if Paystack initialization succeeded
    if not paystack_response.get('status'):
        return Response(
            {"error": "Paystack initialization failed", "details": paystack_response},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Success
    return Response({
        "authorization_url": paystack_response['data']['authorization_url'],
        "reference": order.reference
    }, status=status.HTTP_201_CREATED)

