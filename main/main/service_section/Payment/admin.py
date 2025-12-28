from django.contrib import admin
from service_section.Payment.models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'paystack_reference')
    list_filter = ('status',)
    search_fields = ('paystack_reference',)