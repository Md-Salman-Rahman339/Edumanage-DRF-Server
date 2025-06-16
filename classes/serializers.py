from rest_framework import serializers
from .models import Class, MyClass
from users.serializers import UserSerializer

class ClassSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    
    class Meta:
        model = Class
        fields = '__all__'

class MyClassSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    
    class Meta:
        model = MyClass
        fields = '__all__'
        read_only_fields = ['teacher', 'status', 'total_enrolment']

class CreateMyClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyClass
        fields = ['title', 'short_description', 'price', 'image']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['teacher'] = request.user
        return super().create(validated_data)