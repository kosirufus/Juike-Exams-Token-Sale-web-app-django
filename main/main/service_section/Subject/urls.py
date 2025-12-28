from django.urls import path
from .views import list_subjects

urlpatterns = [
    path('subjects/', list_subjects),
]
