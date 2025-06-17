from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home
urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/classes/', include('classes.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/enrollments/', include('enrollments.urls')),
    path('api/assignments/', include('assignments.urls')),
    path('api/submissions/', include('submissions.urls')),
]