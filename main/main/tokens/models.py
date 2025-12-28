from django.db import models
from product.models import Product

# Create your models here.
class Token(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    assigned = models.BooleanField(default=False)

    
