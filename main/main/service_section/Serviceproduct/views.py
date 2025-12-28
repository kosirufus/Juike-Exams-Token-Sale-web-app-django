# service_section/Serviceproduct/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ServiceProduct
from rest_framework import status

@api_view(['GET'])
def list_products(request):
    products = ServiceProduct.objects.filter(is_active=True)
    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price)  # convert Decimal to float for frontend
        } for p in products
    ]
    return Response(data, status=status.HTTP_200_OK)
