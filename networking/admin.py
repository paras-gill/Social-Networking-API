from django.contrib import admin
from .models import CustomUser, FriendRequest

admin.site.register(CustomUser)
admin.site.register(FriendRequest)
