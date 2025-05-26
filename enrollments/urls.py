from django.urls import path
from .views import EnrollmentListView, EnrollmentCreateView

urlpatterns = [
    path('', EnrollmentListView.as_view(), name='enrollment-list'),
    path('create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
]