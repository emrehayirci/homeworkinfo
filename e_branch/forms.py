from django.contrib.auth.forms import UserCreationForm
from users.models import User
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