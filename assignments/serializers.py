from rest_framework import serializers
from .models import Assignment
from classes.models import Class  
from classes.serializers import ClassSerializer

class AssignmentSerializer(serializers.ModelSerializer):
    class_obj = ClassSerializer(read_only=True)
    
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentCreateSerializer(serializers.ModelSerializer):
    class_obj = ClassSerializer(read_only=True)  
    class_obj_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(), write_only=True, source='class_obj'
    )

    class Meta:
        model = Assignment
        fields = ['class_obj', 'class_obj_id', 'title', 'description', 'due_date']
    
    def create(self, validated_data):
        assignment = super().create(validated_data)
        
       
        class_obj = assignment.class_obj
        class_obj.assignment_count += 1
        class_obj.save()
        
        return assignment
