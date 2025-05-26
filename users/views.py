from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, TeacherRequest
from .serializers import UserSerializer, TeacherRequestSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdmin, IsTeacher, IsStudent

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'email'

class MakeAdminView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.role = 'admin'
        user.save()
        return Response({'status': 'User role updated to admin'})

class CheckAdminView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        email = kwargs.get('email')
        if request.user.email != email:
            return Response({'detail': 'Unauthorized access'}, status=403)
        return Response({'admin': request.user.role == 'admin'})

class CheckTeacherView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        email = kwargs.get('email')
        if request.user.email != email:
            return Response({'detail': 'Unauthorized access'}, status=403)
        return Response({'teacher': request.user.role == 'teacher'})

class CheckStudentView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        email = kwargs.get('email')
        if request.user.email != email:
            return Response({'detail': 'Unauthorized access'}, status=403)
        return Response({'student': request.user.role in ['student', None]})

class TeacherRequestCreateView(generics.CreateAPIView):
    queryset = TeacherRequest.objects.all()
    serializer_class = TeacherRequestSerializer
    permission_classes = [IsAuthenticated]

class TeacherRequestListView(generics.ListAPIView):
    queryset = TeacherRequest.objects.all()
    serializer_class = TeacherRequestSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class ApproveTeacherRequestView(generics.UpdateAPIView):
    queryset = TeacherRequest.objects.all()
    serializer_class = TeacherRequestSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'approved'
        instance.save()
        
        # Update user role
        user = instance.user
        user.role = 'teacher'
        user.save()
        
        return Response({'status': 'Request approved and user role updated'})

class RejectTeacherRequestView(generics.UpdateAPIView):
    queryset = TeacherRequest.objects.all()
    serializer_class = TeacherRequestSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'rejected'
        instance.save()
        return Response({'status': 'Request rejected'})