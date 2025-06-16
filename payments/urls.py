from django.urls import path
from .views import CreatePaymentIntentView, PaymentConfirmView,UserPaymentHistoryView,AdminPaymentHistoryView

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('confirm/', PaymentConfirmView.as_view(), name='payment-confirm'),
    path('history/<str:email>/', UserPaymentHistoryView.as_view(), name='user-payment-history'),
    path('admin/', AdminPaymentHistoryView.as_view(), name='admin-payment-history'),
]