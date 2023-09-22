from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User, Group, Permission
from django.db import models

class GameDataUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class GameData(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=15, null=True)
    lastgame = models.FloatField(null=True, default=0.0)
    current_score = models.FloatField(null=True, default=0.0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add any additional fields you need for authentication

    objects = GameDataUserManager()

    USERNAME_FIELD = 'username'

    # Specify unique related names for the groups and user_permissions fields
    groups = models.ManyToManyField(Group, blank=True, related_name='game_data_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='game_data_users_permissions')

    def __str__(self):
        return self.username
