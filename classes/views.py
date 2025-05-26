from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Class, MyClass
from .serializers import ClassSerializer, MyClassSerializer, CreateMyClassSerializer
from users.permissions import IsAdmin, IsTeacher, IsStudent

class ClassListView(generics.ListAPIView):
    queryset = Class.objects.filter(status='approved')
    serializer_class = ClassSerializer
    permission_classes = [permissions.AllowAny]

class ClassDetailView(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.AllowAny]

class MyClassListView(generics.ListAPIView):
    serializer_class = MyClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MyClass.objects.filter(teacher=self.request.user)

class MyClassCreateView(generics.CreateAPIView):
    serializer_class = CreateMyClassSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class MyClassDeleteView(generics.DestroyAPIView):
    queryset = MyClass.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    
    def get_queryset(self):
        return super().get_queryset().filter(teacher=self.request.user)

class PendingClassListView(generics.ListAPIView):
    queryset = MyClass.objects.filter(status='pending')
    serializer_class = MyClassSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class ApproveClassView(generics.UpdateAPIView):
    queryset = MyClass.objects.all()
    serializer_class = MyClassSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'approved'
        instance.save()
        
        # Create a corresponding approved class
        Class.objects.create(
            title=instance.title,
            description=instance.description,
            teacher=instance.teacher,
            price=instance.price,
            seats=instance.seats,
            status='approved'
        )
        
        return Response({'status': 'Class approved'})

class RejectClassView(generics.UpdateAPIView):
    queryset = MyClass.objects.all()
    serializer_class = MyClassSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'rejected'
        instance.save()
        return Response({'status': 'Class rejected'})