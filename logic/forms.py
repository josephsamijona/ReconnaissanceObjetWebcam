# logic/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignupForm(UserCreationForm):
    """
    Form for user signup, extending the default UserCreationForm to include email.
    """
    email = forms.EmailField(required=True, help_text='Requis. Entrez une adresse email valide.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class APIKeyForm(forms.ModelForm):
    """
    Form to update the Hugging Face API key.
    """
    class Meta:
        model = UserProfile
        fields = ['huggingface_api_key']
        widgets = {
            'huggingface_api_key': forms.PasswordInput(attrs={'placeholder': 'Entrez votre clé API Hugging Face'}),
        }
