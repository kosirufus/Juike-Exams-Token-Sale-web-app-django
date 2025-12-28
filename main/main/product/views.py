from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .models import Product
from django.views.decorators.cache import never_cache

@never_cache
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
        return Response({
            'id': product.id,
            'name': product.display_name,
            'price': product.price,
        })
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
