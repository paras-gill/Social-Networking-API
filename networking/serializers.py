from django.contrib.auth import get_user_model
from rest_framework import serializers 
from .models import CustomUser, FriendRequest


User = get_user_model()


# Serializer for CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'password']  
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # email should be unique to every user
        email = data['email'].lower()  #
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email address is already in use.")
        
        # Name should not contain special character and numbers
        special_characters = "1234567890!@#$%^&*()-+?=,<>/"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('Name cannot contain numbers or special chars')
        
        return data 

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'].lower(),
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Serializer for handling user login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True) 


# Serializer for FriendRequest model
class FriendRequestSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    receiver = CustomUserSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'sent_at', 'pending_status', 'response_status', 'responded_at']