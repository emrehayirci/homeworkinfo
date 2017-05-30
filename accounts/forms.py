from django import forms
from .models import Accounts, Currency, ACCOUNT_TYPE_CHOICES


class AccountForm(forms.ModelForm):
    
    iban = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # account_type = forms.TypedMultipleChoiceField(choices=ACCOUNT_TYPE_CHOICES,
    #                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Accounts
        fields = ('iban', 'amount')
