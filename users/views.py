from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, TeacherRequest
from .serializers import UserSerializer, TeacherRequestSerializer,CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from .permissions import IsAdmin, IsTeacher, IsStudent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
User = get_user_model()

# class FirebaseTokenExchangeView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         if not email:
#             return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user = User.objects.get(email=email)
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh)
#             })
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # Log validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return Response({
        #     'user': UserSerializer(user, context=self.get_serializer_context()).data,
        #     'message': 'User created successfully'
        # }, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'email'

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  

class UserByEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email query parameter is required'}, status=400)
        try:
            user = User.objects.get(email=email)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)      

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
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')

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