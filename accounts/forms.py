from django import forms
from django.contrib.auth.models import User
from shop.models import Vendor

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

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
        
        