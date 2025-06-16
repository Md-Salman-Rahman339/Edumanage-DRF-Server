from rest_framework import serializers
from .models import Payment
from classes.serializers import ClassSerializer
from users.serializers import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class_obj = ClassSerializer(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    date = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = Payment
        fields = ['id','email', 'user', 'class_obj', 'title', 'amount', 'transaction_id', 'status','date', 'created_at']

class CreatePaymentIntentSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    class_id = serializers.IntegerField(required=True)