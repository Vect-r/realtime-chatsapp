from django import forms
from .models import *
from apps.master.utils.inputValidators import *

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True,max_length=100)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Validate email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return is_valid_email(email)

    # Validate username uniqueness
    def clean_username(self):
        name = self.cleaned_data.get('username')
        if User.objects.filter(username=name).exists():
            raise ValidationError("Username already exists.")
        return name

    # Validate password strength
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return validatePassword(password)

    # Cross-field validation (password match)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            match_password(password, confirm_password)

        return cleaned_data