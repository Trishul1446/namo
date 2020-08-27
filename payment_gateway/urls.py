from django.urls import path
from payment_gateway.views import PaymentGateway

urlpatterns = [
    path("paymentGateway", PaymentGateway.as_view(), name="payment_gateway")
]
