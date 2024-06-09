from django.contrib.auth import get_user_model, authenticate  
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, throttle_classes 
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CustomUserSerializer, LoginSerializer, FriendRequestSerializer
from .models import FriendRequest

User = get_user_model()



# View for user registration
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]  # No authentication required
    def post(self, request):
        serializer = CustomUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully","data": serializer.data}, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
