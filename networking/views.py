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



# View for user login
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]  # No authentication required
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request=request, email=email, password=password)
            if user: 
                refresh = RefreshToken.for_user(user)  # Generate JWT tokens
                return Response({
                    "message": "User logged in successfully",
                    'access': str(refresh.access_token),  # Access token issued by authentication server upon login
                    #'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid login credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# View for searching users
class UserSearchAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]   # Use JWT for authentication
    permission_classes = [permissions.IsAuthenticated]   # Only authenticated users can access
    pagination_class = PageNumberPagination  # Enable pagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return User.objects.filter(
            Q(email__iexact=query) | Q(name__icontains=query)   # Search by email or name-starting -with query
        ).distinct()

    def paginate_queryset(self, queryset):
        page_size = 10   # Set page size
        paginator = self.paginator
        paginator.page_size = page_size
        return paginator.paginate_queryset(queryset, self.request, view=self)



# View for sending friend requests
@api_view(['POST'])
@authentication_classes([JWTAuthentication])    # Use JWT for authentication
@permission_classes([permissions.IsAuthenticated])    # Only authenticated users can access
@throttle_classes([UserRateThrottle])   # Apply rate throttling
def send_friend_request(request, receiver_id):
    sender = request.user
    try:
        receiver = User.objects.get(id=receiver_id)
    except ObjectDoesNotExist:
        return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if sender.id == receiver.id:
        return Response({"error": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

    friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
    if not created:
        return Response({"error": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"success": "Friend request sent."}, status=status.HTTP_201_CREATED)



# View for listing pending friend requests
@api_view(['GET'])
@authentication_classes([JWTAuthentication])    # Use JWT for authentication
@permission_classes([permissions.IsAuthenticated])   # Only authenticated users can access
def list_pending_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(receiver=request.user, pending_status=True)
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# View for responding to friend requests
@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])   # Use JWT for authentication
@permission_classes([permissions.IsAuthenticated])   # Only authenticated users can access
def respond_friend_request(request, request_id, action):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
    except FriendRequest.DoesNotExist:
        return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

    if not friend_request.pending_status:
        return Response({"error": "This friend request has already been responded to."}, status=status.HTTP_400_BAD_REQUEST)
    
    action = bool(action)
    friend_request.response_status = action 
    friend_request.pending_status = False
    friend_request.responded_at = timezone.now()
    friend_request.save()
    return Response({"success": "Friend request responded to."}, status=status.HTTP_200_OK)



# View for listing friends
@api_view(['GET'])
@authentication_classes([JWTAuthentication])  
@permission_classes([permissions.IsAuthenticated])
def list_friends(request):
    friends = User.objects.filter(
        Q(sent_friend_requests__receiver=request.user, sent_friend_requests__response_status=True) |
        Q(received_friend_requests__sender=request.user, received_friend_requests__response_status=True)
    ).distinct()
    serializer = CustomUserSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

