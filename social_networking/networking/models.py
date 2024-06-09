from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)


# Custom user model extending Django's AbstractUser
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

# Model for handling friend requests between users
class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_friend_requests', on_delete=models.CASCADE)   # User sending the friend request
    receiver = models.ForeignKey(CustomUser, related_name='received_friend_requests', on_delete=models.CASCADE)   # User receiving the friend request
    sent_at = models.DateTimeField(auto_now_add=True)     # Time when the request was sent
    pending_status = models.BooleanField(default=True)     # True if request is pending, False if responded
    response_status = models.BooleanField(null=True, blank=True)      # True for accepted, False for rejected, Null if pending
    responded_at = models.DateTimeField(null=True, blank=True)       # Time when the request was responded

