from django.db import models
from tokens.models import Token
from product.models import Product
import uuid

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING')  # PENDING, PAID
    reference = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__ (self):
        return str(self.reference)

class AssignedToken(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
