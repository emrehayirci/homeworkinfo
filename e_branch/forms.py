from datetime import date, timedelta
from random import Random
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from accounts.models import Accounts, Loan, Transaction, LoanAccountPayment, Currency
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms


def generate_iban():
    random = Random()
    result = 'TR24'
    for i in range(0, 4):
        result += ' '
        for j in range(0, 4):
            result += str(random.randint(0, 9))
    return result


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
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

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

    def save(self, user, commit=True):
        instance = super(AccountCreationForm, self).save(commit=False)
        instance.iban = generate_iban()
        instance.amount = 0
        instance.created_at = date.today()
        instance.user = user
        if commit:
            instance.save()
        return instance


class LoanCreationForm(forms.Form):
    amount = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    installment = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoanCreationForm, self).__init__(*args, **kwargs)

    def clean(self):
        amount = self.cleaned_data.get("amount")
        installment = self.cleaned_data.get("installment")
        user = self.request.user
        if not amount or not installment:
            return self.cleaned_data

        new_loan = Loan()
        new_loan.amount = int(amount)
        new_loan.installment = int(installment)
        new_loan.start_date = date.today()
        new_loan.finish_date = date.today() + timedelta(weeks=4 * int(installment))
        new_loan.interest_rate = 0.2

        loan_account = Accounts()
        loan_account.iban = generate_iban()
        loan_account.account_type = "Loan Account"
        loan_account.amount = int(amount)
        loan_account.created_at = date.today()
        loan_account.currency_type = Currency.objects.first()
        loan_account.user = user
        loan_account.save()
        new_loan.account = loan_account
        new_loan.save()
        for i in range(1, int(installment) + 1):
            monthlypayment = LoanAccountPayment()
            monthlypayment.account = loan_account
            monthlypayment.finish_date = date.today() + timedelta(weeks=(4 * i))
            monthlypayment.installment_number = i
            monthlypayment.is_paid = False
            monthlypayment.is_active = True
            monthlypayment.loan = new_loan
            monthlypayment.amount = 1.2 * (int(amount) / int(installment))
            monthlypayment.save()
        return self.cleaned_data


class TransactionCreationForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sourceiban = forms.ModelChoiceField(queryset=Accounts.objects.all(),
                                        widget=forms.Select(attrs={'class': "form-control"}))
    destinationiban = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TransactionCreationForm, self).__init__(*args, **kwargs)

        if self.request:
            self.fields['sourceiban'].queryset = Accounts.objects.filter(user=self.request.user)

    def clean(self):
        description = self.cleaned_data.get("description")
        amount = self.cleaned_data.get("amount")
        source = self.cleaned_data.get("sourceiban")
        destinationiban = self.cleaned_data.get("destinationiban")
        if source.user != self.request.user:
            raise ValidationError("This is not your Account")
        try:
            destination = Accounts.objects.get(iban = destinationiban)
        except Accounts.DoesNotExist:
            raise ValidationError("Wrong Destination IBAN")
        if source.amount > amount:
            transaction = Transaction()
            transaction.amount = amount
            transaction.description = description
            transaction.sourceaccount = source
            transaction.destinationaccount = destination
            transaction.currency_type = source.currency_type
            transaction.sending_date = date.today()
            transaction.make_transaction()
        else:
            raise ValidationError("Not Enough Account Balance")
