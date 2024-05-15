# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Person

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'mail', 'date_of_birth', 'hobby']
