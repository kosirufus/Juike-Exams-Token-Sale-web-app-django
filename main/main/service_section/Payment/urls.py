# payments/urls.py
from django.urls import path
from .views import create_payment

urlpatterns = [
    path('pay/', create_payment),
]
