from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),  # list all
    path('<int:id>/', views.product_detail, name='product-detail'),  # single product
]
