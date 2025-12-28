# service_section/Serviceproduct/urls.py
from django.urls import path
from .views import list_products

urlpatterns = [
    path('serviceproducts/', list_products, name='list-serviceproducts'),
]
