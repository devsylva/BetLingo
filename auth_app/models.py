import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import UserManager
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?234\d{11}$', message="Nigerian phone number must start with '+234' followed by 11 digits.") 
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    

    def __str__(self):
        return self.email
    