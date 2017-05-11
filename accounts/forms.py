from django import forms
from .models import Accounts, Currency

CURRENCIES = Currency.objects.filter().values_list('id', 'currency_type')

class AccountForm(forms.ModelForm):
    
    iban = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    account_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    currency_type_id = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices=CURRENCIES,
    )
    class Meta:
        model = Accounts
        fields = ('iban', 'account_type', 'currency_type_id', 'amount')
