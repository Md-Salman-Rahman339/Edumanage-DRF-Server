from rest_framework import serializers
from .models import Submission
from assignments.serializers import AssignmentSerializer
from users.serializers import UserSerializer

class SubmissionSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    
    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['assignment', 'content']
        extra_kwargs = {
            'assignment': {'source': 'assignment_id', 'write_only': True}
        }
    
    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)