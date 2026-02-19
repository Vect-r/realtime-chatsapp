from django.db import models
from apps.master.models import BaseClass

# Create your models here.
class User(BaseClass):
    username = models.CharField(null=False,blank=False,max_length=255)
    password = models.CharField(null=False,blank=False,max_length=255)
    email = models.EmailField(null=False,blank=False,max_length=255)
    isActive = models.BooleanField(default=False)
    bio = models.TextField(max_length=200)