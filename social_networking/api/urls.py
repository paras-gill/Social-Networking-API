from django.urls import path
from networking.views import LoginView, RegisterView, UserSearchAPIView,send_friend_request, respond_friend_request, list_friends, list_pending_friend_requests

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
]