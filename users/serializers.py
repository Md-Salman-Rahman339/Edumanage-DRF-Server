from rest_framework import serializers
from .models import User, TeacherRequest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],  
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            role=validated_data.get('role', 'student')
        )
        return user

class TeacherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherRequest
        fields = '__all__'