from rest_framework import generics, permissions,serializers
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer
from users.permissions import IsStudent
from django.shortcuts import get_object_or_404
from classes.models import Class 
class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

class EnrollmentAfterPaymentView(generics.CreateAPIView):
    serializer_class = EnrollmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def perform_create(self, serializer):
        class_id = self.kwargs['pk']
        class_obj = get_object_or_404(Class, id=class_id)
           # Check if the user is already enrolled
        if Enrollment.objects.filter(user=self.request.user, class_obj=class_obj).exists():
            raise serializers.ValidationError("You are already enrolled in this class.")
        
        serializer.save(user=self.request.user, class_obj=class_obj)
        class_obj.total_enrolment += 1
        class_obj.save()


class UserEnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        email = self.kwargs.get('email')
        if self.request.user.email != email:
            return Enrollment.objects.none() 
        return Enrollment.objects.filter(user__email=email).select_related('class_obj')