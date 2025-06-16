from django.urls import path
from .views import (
    ClassListView,
    ClassDetailView,
    MyClassListView,
    MyClassCreateView,
    MyClassDeleteView,
    PendingClassListView,
    ApproveClassView,
    RejectClassView,
    ApprovedMyClassListView,
    MyClassDetailView,
    MyApprovedClassListView

)

urlpatterns = [
    path('', ClassListView.as_view(), name='class-list'),
    path('<int:pk>/', ClassDetailView.as_view(), name='class-detail'),
    path('my-classes/', MyClassListView.as_view(), name='my-class-list'),
    path('my-classes/approved/', ApprovedMyClassListView.as_view(), name='my-class-approved'),
    path('my-classes/details/<int:pk>/', MyClassDetailView.as_view(), name='my-class-detail'),
    path('my-classes/create/', MyClassCreateView.as_view(), name='my-class-create'),
    path('my-classes/delete/<int:pk>/', MyClassDeleteView.as_view(), name='my-class-delete'),
    path('pending-classes/', PendingClassListView.as_view(), name='pending-class-list'),
    path('approve-class/<int:pk>/', ApproveClassView.as_view(), name='approve-class'),
    path('my-approved-classes/', MyApprovedClassListView.as_view(), name='my-approved-class-list'),
    path('reject-class/<int:pk>/', RejectClassView.as_view(), name='reject-class'),
]