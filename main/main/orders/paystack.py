import requests
from django.conf import settings

PAYSTACK_SECRET_KEY=settings.PAYSTACK_SECRET_KEY
BASE_URL = "https://api.paystack.co"

def initialize_transaction (email, amount, reference):
    url = f"{BASE_URL}/transactions/initialize"
    headers = {
        "Authorization": f"Bearer{settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "amount": amount,
        "reference": reference,
    }
    res = requests.post (url, json = data, headers = headers)
    return res.json()

# function to verify if payment was successful
"""THe verification function beliow does not verify payments itself, it only asks paystack 
for the payment status"""

def verify_transaction (reference):
    url = f"{BASE_URL}/transactions/verify/{reference}"
    headers = {
        "Authorization": f"Bearer{PAYSTACK_SECRET_KEY}"
    }
    res = requests.get (url, headers = headers)
    return res.json()
    