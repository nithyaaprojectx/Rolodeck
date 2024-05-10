# forms.py
from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'organization', 'hobby','date_of_birth','mail','phone_number','interests','notes']  # Add other fields as needed
