from rest_framework import serializers
from .models import Assignment
from classes.serializers import ClassSerializer

class AssignmentSerializer(serializers.ModelSerializer):
    class_obj = ClassSerializer(read_only=True)
    
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['class_obj', 'title', 'description', 'due_date']
        extra_kwargs = {
            'class_obj': {'source': 'class_obj_id', 'write_only': True}
        }
    
    def create(self, validated_data):
        assignment = super().create(validated_data)
        
        # Increment assignments count for the class
        class_obj = assignment.class_obj
        class_obj.assignments_count += 1
        class_obj.save()
        
        return assignment