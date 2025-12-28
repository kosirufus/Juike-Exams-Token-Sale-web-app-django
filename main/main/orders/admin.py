from django.contrib import admin
from .models import Order, AssignedToken

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'amount', 'status')
    list_filter = ('status',)
    search_fields = ('id', 'product__name')

@admin.register(AssignedToken)
class AssignedTokenAdmin(admin.ModelAdmin):
    list_display = ('order', 'token')
    search_fields = ('token__code',)
