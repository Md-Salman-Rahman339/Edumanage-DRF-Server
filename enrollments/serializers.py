from rest_framework import serializers
from .models import Enrollment
from classes.serializers import ClassSerializer
from users.serializers import UserSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class_obj = ClassSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['class_obj']
        extra_kwargs = {
            'class_obj': {'source': 'class_obj_id', 'write_only': True}
        }
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)