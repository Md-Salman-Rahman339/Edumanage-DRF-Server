from rest_framework import serializers
from .models import User, TeacherRequest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role if hasattr(user,'role') else 'student'
        return token

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)  

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'name', 'role', 'password', 'photo']
        extra_kwargs = {'password': {'write_only': True}, 'first_name': {'required': False},
    'last_name': {'required': False},
    'photo': {'required': False},
    'username': {'required': True},}
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'student'),
            photo=validated_data.get('photo', '')
        )
        return user

class TeacherRequestSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = TeacherRequest
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 
                 'name', 'image', 'experience', 'title', 'category']
        extra_kwargs = {
            'user': {'read_only': True},  
            'status': {'read_only': True},  
        }
    
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
    def get_experience(self, obj):
        return obj.user.experience
    
    def get_image(self, obj):
        return obj.user.photo if obj.user.photo else None
