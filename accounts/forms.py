from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from shop.models import Vendor
import re

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        help_text="Password must be at least 8 characters long"
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores.")
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise forms.ValidationError("First name can only contain letters and spaces.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise forms.ValidationError("Last name can only contain letters and spaces.")
        return last_name

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return confirm_password

class VendorRegisterForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['shop_name', 'logo', 'banner_image', 'phone_number', 'location', 'address']
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        # We only allow editing these fields. Username changes can be complex,
        # and password changes should have their own dedicated, secure form.
        fields = ['first_name', 'last_name', 'email']
        
        