# models.py
from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    hobby = models.CharField(max_length=100)
    # Add other details as needed

    def __str__(self):
        return self.name
