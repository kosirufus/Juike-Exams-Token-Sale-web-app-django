from django.db import models
from django.utils import timezone
from service_section.Serviceproduct.models import ServiceProduct
from service_section.Serviceorder.models import ServiceOrder
import uuid


# 🔹 Named function (Django can serialize this)
def default_expiry_time():
    return timezone.now() + timezone.timedelta(minutes=15)


class WhatsappGroup(models.Model):
    CLASS_CHOICES = (
        ('science', 'Science'),
        ('art', 'Art'),
    )

    product = models.ForeignKey(ServiceProduct, on_delete=models.CASCADE)
    student_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    group_link = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.student_class}"


class WhatsAppAccessToken(models.Model):
    order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    joined_groups = models.ManyToManyField(
        WhatsappGroup,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry_time)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def all_groups_joined(self):
        allowed_groups = WhatsappGroup.objects.filter(
            product__in=self.order.products.all(),
            student_class=self.order.student_class,
            is_active=True
        ).count()

        return self.joined_groups.count() >= allowed_groups

    def __str__(self):
        return f"{self.order.reference} - {self.token}"
