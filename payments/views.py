import stripe
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentSerializer, CreatePaymentIntentSerializer, PaymentCreateSerializer
from classes.models import Class
from users.permissions import IsAdmin, IsStudent

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def post(self, request):
        serializer = CreatePaymentIntentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        amount = int(serializer.validated_data['price'] * 100)
        
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card']
            )
            return Response({
                'clientSecret': payment_intent.client_secret
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def perform_create(self, serializer):
        class_obj_id = serializer.validated_data['class_obj_id']
        class_obj = Class.objects.get(id=class_obj_id)
        
        # Decrease available seats
        class_obj.seats -= 1
        class_obj.total_enrolment += 1
        class_obj.save()
        
        serializer.save(
            user=self.request.user,
            class_obj=class_obj,
            status='success'
        )

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)

class AdminPaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]