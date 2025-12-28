from django.urls import path
from .views import (
    create_paystack_session,
    verify_paystack,
    assigned_tokens,
)

urlpatterns = [
    path("create-paystack-session/", create_paystack_session),
    path("verify-paystack/", verify_paystack),
    path("assigned-tokens/", assigned_tokens),
]
