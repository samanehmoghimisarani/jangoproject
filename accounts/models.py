from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    family = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)    # دستیار
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'name', 'family']
    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin
