# models.py
from django.db import models
from django.contrib.auth.models import User
import datetime
class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    hobby = models.CharField(max_length=100)
    date_of_birth = models.DateField(default=datetime.date.today)
    phone_number = models.CharField(max_length=100, default="995055555")
    mail = models.CharField(max_length=100,default="abc@gmail.com")
    interests = models.CharField(max_length=100, default="fill it")
    notes = models.CharField(max_length=100,default="fill it")
    # Add other details as needed

    def __str__(self):
        return self.name
