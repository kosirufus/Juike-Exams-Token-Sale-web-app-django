from django.db import models
from service_section.Serviceorder.models import ServiceOrder

# Create your models here.
class Payment(models.Model):
    order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE)
    paystack_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    paid_at = models.DateTimeField(auto_now_add=True)