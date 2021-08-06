from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin, AbstractBaseUser, UserManager)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from todolistapi.apps.helpers.models import TrackingModel

class MyUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('the given username must be set')

        if not email:
            raise ValueError('the given email must be set')

        email = self.normalize_email(email)
        username = self.nomalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)
        

class User(AbstractBaseUser, PermissionsMixin,TrackingModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150, 
        unique=True, 
        validators=[username_validator], 
    )
    email = models.EmailField(
        blank=False, 
        unique=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)
    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user']

    @property
    def token(self):
        pass