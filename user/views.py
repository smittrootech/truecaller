from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from .models import User
from .user_defined_func.Custom_authentication import CustomeAuthentication
from django.contrib.auth import get_user_model

# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         mobile_number = serializer.validated_data['mobile_number']
#         try:
#             existing_user = User.objects.get(mobile_number=mobile_number)
#             # Handle the case when a user with the given mobile number already exists
#             return Response({'error': 'User with this mobile number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist:
#             # Generate OTP
#             otp = random.randint(1000, 9999)
#             print(serializer)
#             # Save the OTP in the user object
#             user = serializer.save(otp=otp)

#             # Send OTP to the user via SMS using Twilio (example)
#             client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#             message = client.messages.create(
#                 body=f'Your OTP: {otp}',
#                 from_=settings.TWILIO_PHONE_NUMBER,
#                 to=mobile_number
#             )

#             return Response({'message': 'OTP has been sent to your mobile number.'})


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
    

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        serializer = CustomeAuthentication(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['mobile_number']
        try:
            user = User.objects.get(mobile_number=user)
        except User.DoesNotExist:
            # Handle the case when the user doesn't exist
            # Return an appropriate response or raise an exception
            # Example: return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            pass

        print(login(request, user))
        return super(LoginAPI, self).post(request, format=None)
    


