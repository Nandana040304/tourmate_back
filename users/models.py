from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
import uuid
from django.utils import timezone
from datetime import timedelta



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # remove username

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    medical_condition = models.TextField(blank=True, null=True)
    emergency_contact1 = models.CharField(max_length=15)
    emergency_contact2 = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()   # 👈 VERY IMPORTANT

    def __str__(self):
        return self.full_name

class PasswordReset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=15)
    