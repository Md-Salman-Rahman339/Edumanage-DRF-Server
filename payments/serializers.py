from rest_framework import serializers
from .models import Payment
from classes.serializers import ClassSerializer
from users.serializers import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class_obj = ClassSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'

class CreatePaymentIntentSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class_id = serializers.IntegerField()

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['class_obj', 'amount', 'transaction_id']
        extra_kwargs = {
            'class_obj': {'source': 'class_obj_id', 'write_only': True}
        }
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'success'
        return super().create(validated_data)