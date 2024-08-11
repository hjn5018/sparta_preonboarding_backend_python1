from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .serializers import LoginRequestSerializer, LoginResponseSerializer, SignupRequestSerializer, SignupResponseSerializer
from .models import Role, UserRole
from drf_spectacular.utils import extend_schema

class SignupAPIView(APIView):
    @extend_schema(
            request=SignupRequestSerializer,
            responses={status.HTTP_201_CREATED: SignupResponseSerializer}
    )
    def post(self, request):
        data = request.data
        user = get_user_model().objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            nickname=data.get('nickname'),
        )
        
        default_role, created = Role.objects.get_or_create(role='USER')
        UserRole.objects.create(user=user, role=default_role)

        serializer = SignupResponseSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LoginAPIView(APIView):
    @extend_schema(
            request=LoginRequestSerializer,
            responses={status.HTTP_200_OK: LoginResponseSerializer}
    )
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})
        return Response({"detail": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
