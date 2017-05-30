from django.contrib.auth.forms import UserCreationForm
from users.models import User
from accounts.models import Accounts, Loan,Transaction,LoanAccountPayment
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        fields = ['email', 'first_name', 'last_name', 'identity_number']
        model = User

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['identity_number'].widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if not email or not password:
            return self.cleaned_data

        user = authenticate(email=email,
                            password=password)

        if user:
            self.user = user
        else:
            raise ValidationError("Yanlış kullanıcı adı veya şifre!")

        return self.cleaned_data


class AccountCreationForm(ModelForm):
    class Meta:
        model = Accounts
        fields = [
            'account_type',
            'currency_type',
        ]

    def __init__(self, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)
        self.fields['account_type'].widget.attrs['class'] = 'form-control'
        self.fields['currency_type'].widget.attrs['class'] = 'form-control'
