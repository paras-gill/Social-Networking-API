from django.urls import path
from networking.views import LoginView, RegisterView, UserSearchAPIView,send_friend_request, respond_friend_request, list_friends, list_pending_friend_requests

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-request/send/<int:receiver_id>/', send_friend_request, name='send-friend-request'),
    path('friend-requests/pending/', list_pending_friend_requests, name='list-pending-friend-requests'),
    path('friend-request/respond/<int:request_id>/<int:action>/', respond_friend_request, name='respond-friend-request'),
    path('friends/', list_friends, name='list-friends'),
]