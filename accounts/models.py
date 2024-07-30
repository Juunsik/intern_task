from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOCIES = (("USER", "User"),)  # User 외 role 추가 가능

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOCIES,
        default="USER",
    )

    username = models.CharField(
        max_length=50,
        unique=True,
    )
    nickname = models.CharField(
        max_length=30,
        unique=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nickname"]

    objects = UserManager()

    def __str__(self):
        return self.username
