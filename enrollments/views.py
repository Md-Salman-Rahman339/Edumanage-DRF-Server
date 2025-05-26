from rest_framework import generics, permissions
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer
from users.permissions import IsStudent

class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]