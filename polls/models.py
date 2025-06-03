from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, phone_number, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+375(?:29|33|44|25|17)\d{7}$', message='Enter a valid phone number.')]
    )
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    services = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    favorites = models.ManyToManyField('properties.Property', related_name='favorited_by', blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.first_name

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return (timezone.now() - self.created_at).seconds > 300  
