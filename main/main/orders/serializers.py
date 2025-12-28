from rest_framework import serializers
from .models import Order, AssignedToken
from tokens.models import Token

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class AssignedTokenSerializer(serializers.ModelSerializer):
    token_code = serializers.CharField(source='token.code', read_only=True)
    
    class Meta:
        model = AssignedToken
        fields = ['id','order','token','token_code','delivered','delivered_at']
