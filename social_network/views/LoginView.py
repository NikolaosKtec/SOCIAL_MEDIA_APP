
from django.contrib.auth import get_user_model

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status,permissions



from ..serializers import ObtainTokenSerializer
from ..management.authentication import JWTAuthentication



User = get_user_model()

class LoginView(APIView):
    # NOTE this class does the login and returns an authentication token
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        
        user = User.objects.filter(username=username_or_email).first()

        # if user is None:
        #     user = User.objects.filter(phone_number=username_or_email).first()
        
        if user is None or not user.password.__eq__(password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)
        return Response({'token': jwt_token})
        
    