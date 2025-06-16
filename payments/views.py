import stripe
from django.conf import settings
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer, CreatePaymentIntentSerializer
from classes.models import Class
from users.models import User
from users.permissions import IsAdmin

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePaymentIntentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        price = serializer.validated_data['price']
        class_id = serializer.validated_data['class_id']

        try:
            
            class_obj = Class.objects.get(id=class_id)
           

            
            intent = stripe.PaymentIntent.create(
                amount=int(float(price) * 100),  
                currency='usd',
                metadata={
                    'user_id': request.user.id,
                    'class_id': class_id,
                    'class_title': class_obj.title,
                },
                description=f"Payment for {class_obj.title}"
            )

            return Response({
                'clientSecret': intent.client_secret,
                'class_title': class_obj.title
            }, status=status.HTTP_200_OK)

        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            transaction_id = data['transaction_id']

        
            payment_intent = stripe.PaymentIntent.retrieve(transaction_id)
            
            if payment_intent.status != 'succeeded':
                return Response(
                    {'error': 'Payment not confirmed by Stripe'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            class_obj = Class.objects.get(id=data['class_id'])

            
            payment = Payment.objects.create(
                user=request.user,
                class_obj=class_obj,
                amount=payment_intent.amount / 100,
                transaction_id=transaction_id,
                title=data.get('title', payment_intent.description),
                status='completed'
            )

           
            class_obj.total_enrolment += 1
            class_obj.save()

            return Response(
                PaymentSerializer(payment).data,
                status=status.HTTP_201_CREATED
            )

        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserPaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_email = self.kwargs.get('email')
        return Payment.objects.filter(user__email=user_email).order_by('-created_at')        
class AdminPaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Payment.objects.all().order_by('-created_at')        