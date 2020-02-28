from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import TwoFAUserManager


class TwoFAUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=42, unique=True)
    email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=10, unique=True)
    objects = TwoFAUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phonenumber']
