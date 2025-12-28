# orders/models.py
from django.db import models
from service_section.Serviceproduct.models import ServiceProduct
from service_section.Subject.models import Subject

class ServiceOrder(models.Model):
    CLASS_CHOICES = (
        ('science', 'Science'),
        ('art', 'Art'),
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField()

    student_class = models.CharField(
        max_length=10,
        choices=CLASS_CHOICES
    )

    products = models.ManyToManyField(ServiceProduct)
    subjects = models.ManyToManyField(Subject)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.reference})"
