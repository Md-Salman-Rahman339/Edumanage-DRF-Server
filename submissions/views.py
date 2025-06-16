# submissions/views.py
from rest_framework import generics, permissions
from .models import Submission
from .serializers import SubmissionSerializer, SubmissionCreateSerializer
from users.permissions import IsStudent

class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        class_id = self.request.query_params.get('assignment__class_obj_id')
        user = self.request.user
        
        if class_id:
            if user.role == 'teacher':
                return Submission.objects.filter(assignment__class_obj_id=class_id)
            else:
                return Submission.objects.filter(
                    assignment__class_obj_id=class_id,
                    student=user
                )
        return Submission.objects.none()

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)