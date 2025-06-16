from django.urls import path
from .views import EnrollmentListView, EnrollmentCreateView,EnrollmentAfterPaymentView,UserEnrollmentListView

urlpatterns = [
    path('enrolled-classes/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('after-payment/<int:pk>/', EnrollmentAfterPaymentView.as_view(), name='enrollment-after-payment'),
    # urls.py
    path('enrolled-classes/<str:email>/', UserEnrollmentListView.as_view(), name='user-enrollments'),
]