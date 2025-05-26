from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    UserListView,
    UserCreateView,
    UserDetailView,
    MakeAdminView,
    CheckAdminView,
    CheckTeacherView,
    CheckStudentView,
    TeacherRequestCreateView,
    TeacherRequestListView,
    ApproveTeacherRequestView,
    RejectTeacherRequestView,
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<str:email>/', UserDetailView.as_view(), name='user-detail'),
    path('users/make-admin/<int:pk>/', MakeAdminView.as_view(), name='make-admin'),
    path('users/admin/<str:email>/', CheckAdminView.as_view(), name='check-admin'),
    path('users/teacher/<str:email>/', CheckTeacherView.as_view(), name='check-teacher'),
    path('users/student/<str:email>/', CheckStudentView.as_view(), name='check-student'),
    path('teacher-request/', TeacherRequestCreateView.as_view(), name='teacher-request-create'),
    path('teacher-requests/', TeacherRequestListView.as_view(), name='teacher-request-list'),
    path('teacher-requests/approve/<int:pk>/', ApproveTeacherRequestView.as_view(), name='approve-teacher-request'),
    path('teacher-requests/reject/<int:pk>/', RejectTeacherRequestView.as_view(), name='reject-teacher-request'),
]