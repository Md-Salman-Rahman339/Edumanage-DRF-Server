from django.urls import path
from .views import (
    CreatePaymentIntentView,
    PaymentCreateView,
    PaymentListView,
    AdminPaymentListView,
)

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('', PaymentCreateView.as_view(), name='payment-create'),
    path('history/', PaymentListView.as_view(), name='payment-list'),
    path('admin/', AdminPaymentListView.as_view(), name='admin-payment-list'),
]