from django.db import models
from django.contrib.auth.models import User
import datetime
import os
import uuid

def generate_code():
    # Custom code generation function to generate a unique code
    return str(uuid.uuid4().hex[:6].upper())

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}.{ext}"
    return os.path.join('person_images', new_filename)

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    education = models.CharField(max_length=100, default="College")
    ventures = models.CharField(max_length=100, default="Ventures")
    hobby = models.CharField(max_length=100)
    date_of_birth = models.DateField(default=datetime.date.today)
    phone_number = models.CharField(max_length=100, default="995055555")
    mail = models.CharField(max_length=100, default="abc@gmail.com")
    interests = models.CharField(max_length=100, default="fill it")
    instagram = models.CharField(max_length=100, default="www.instagram.com")
    twitter = models.CharField(max_length=100, default="www.x.com")
    linkedin = models.CharField(max_length=100, default="www.linkedin.com")
    youtube = models.CharField(max_length=100, default="www.youtube.com")
    address = models.CharField(max_length=500, default="Earth")
    userself = models.BooleanField(default=False)
    projects = models.CharField(max_length=500, default="Fun")
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, default="000000")
    pronouns = models.CharField(max_length=20, default="pronoun/pronoun")
    codeu = models.CharField(max_length=6, default=generate_code)  # Ensure 'unique=True'
    notes = models.CharField(max_length=100, default="fill it")
    profilepic = models.ImageField(upload_to='person_images/', blank=True, null=True,
                              default='person_images/default_person_image.jpg',
                              help_text='Allowed file types: png, jpg, jpeg, gif')

    def __str__(self):
        return self.name

class Photo(models.Model):
    person = models.ForeignKey(Person, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return f"Photo of {self.person.name}"
