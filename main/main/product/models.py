from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    session = models.CharField(max_length=50)  # e.g., 'WAEC 2026 May/June'

    def __str__(self):
        return self.display_name or self.name or "unnamed product"