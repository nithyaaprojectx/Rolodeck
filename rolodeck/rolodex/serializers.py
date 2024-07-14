# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Person
import base64
import os
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Person, Photo
from rest_framework.serializers import Serializer, FileField

class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image']

    def get_profilepic(self, obj):
        request = self.context.get('request')
        if request and obj.profilepic:
            return request.build_absolute_uri(obj.profilepic.url)
        return None
class PersonEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ('profilepic', 'codeu', 'otp', 'is_phone_verified')

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ('user',)  # Mark 'user' field as read-only

    # Ensure 'user' field accepts primary key (usually 'id' or 'pk') of the related User model
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        user = validated_data.pop('user')
        person = Person.objects.create(user=user, **validated_data)
        return person

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password")