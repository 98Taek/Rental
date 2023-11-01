from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import CustomUser


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "password1", "password2"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Password dont match.")
        return cd["password2"]

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if CustomUser.objects.filter(phone_number=data).exists():
            raise forms.ValidationError("Phone number already in use.")
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data
