from rest_framework import generics, permissions
from .models import Assignment
from .serializers import AssignmentSerializer, AssignmentCreateSerializer
from users.permissions import IsTeacher

class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        if class_id:
            return Assignment.objects.filter(class_obj_id=class_id)
        return Assignment.objects.none()

class AssignmentCreateView(generics.CreateAPIView):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]