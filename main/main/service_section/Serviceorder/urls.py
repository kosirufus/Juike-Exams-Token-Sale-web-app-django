# orders/urls.py
from django.urls import path
from .views import order_success, redirect_to_whatsapp

urlpatterns = [
    path('servicesuccess/<str:reference>/', order_success),
    path('whatsapp-redirect/<uuid:token>/', redirect_to_whatsapp, name='whatsapp-redirect'),
]
