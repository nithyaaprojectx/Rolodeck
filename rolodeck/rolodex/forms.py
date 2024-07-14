from django import forms
from .models import Person, Photo

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'name', 'organization', 'hobby', 'date_of_birth', 'mail',
            'phone_number', 'interests', 'notes', 'profilepic',
            'instagram', 'twitter', 'linkedin', 'youtube', 'address',
            'projects', 'pronouns','userself'
        ]

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
