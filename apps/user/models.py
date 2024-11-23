from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from ..portal.models import *
# from . import apps.apps.por
# Create your models here.

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Set a unique related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Set a unique related name
        blank=True,
    )

class UserPortal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
