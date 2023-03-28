from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'email', 'phone_number', 'birth_date', 'social_media', 'location']
