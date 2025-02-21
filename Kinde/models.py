from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    kinde_id = models.CharField(max_length=255, unique=True, null=True, blank=True)