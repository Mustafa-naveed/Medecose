from django import forms
from django.contrib.auth.models import User
from .models import Profile, Contact

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'address']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
