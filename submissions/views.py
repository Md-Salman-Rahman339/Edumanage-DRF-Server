from rest_framework import generics, permissions
from .models import Submission
from .serializers import SubmissionSerializer, SubmissionCreateSerializer
from users.permissions import IsStudent, IsTeacher

class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        assignment_id = self.request.query_params.get('assignment_id')
        if assignment_id:
            return Submission.objects.filter(assignment_id=assignment_id)
        return Submission.objects.none()

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]