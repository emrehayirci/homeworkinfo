from django import forms
from users.models import User, Address


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_no')


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('city', 'district', 'zipcode', 'street', 'no')
