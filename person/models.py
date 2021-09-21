from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from greenadmin.models import GreenAdmin


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.is_verified = False
        user.save()
        greenA = GreenAdmin.objects.create(user=user)
        greenA.save()
        return user


class GreenUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
     ('admin', 'admin'),
     ('loader', 'loader'),
     ('supplier', 'supplier'),
     ('manager', 'manager'),
    )

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    # first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    # about = models.TextField(_(
    #     'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=40,choices=USER_TYPE_CHOICES, default='admin')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

