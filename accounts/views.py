from django.shortcuts import render, redirect
from .forms import AccountForm
from .models import Accounts, Currency
from IPython import embed
from users.models import User
# Create your views here.


def settings(request):
    if request.method == 'POST':
        form = AccountForm()
        currencies = Currency.objects.all()
        return render(request, 'create_account.html', {'accountform': form, 'currencies': currencies})
    accounts = Accounts.objects.all()
    return render(request, 'settings/court_list.html', {'accounts': accounts})


def create_account(request):
    form = AccountForm(request.POST)
    if request.method == 'GET':
        form = AccountForm()
        users = User.objects.all()
        return render(request, 'create_account.html', {'accountform': form, 'users': users})
    elif request.method == 'POST':
        if form.is_valid():
            currency = Currency.objects.filter(pk=request.POST.get('currency_type'))
            if len(currency) > 0:
                currency = currency[0]
            else:
                currency = Currency.objects.first()
            Accounts.objects.create(iban=request.POST.get('iban'), account_type=request.POST.get('account_type'),
                                    user_id=request.POST.get('user_id'), currency_type=currency,
                                    amount=request.POST.get('amount'))
            # account = form.save(user=request.user)
            # account.currency_type = currency
            # account.user = request.user
            # account.save()
            return redirect('settings')
    else:
        return redirect('settings')


def account_delete(request, pk):
    account = Accounts.objects.get(pk=pk)
    account.delete()
    return redirect('settings')


def account_update(request, pk):
    if request.method == 'GET':
        account = Accounts.objects.get(pk=pk)
        currency = account.currency_type
        currencies = Currency.objects.exclude(id=currency.id)
        user = account.user
        users = User.objects.exclude(id=user.id)
        form = AccountForm(initial={'iban': account.iban, 'account_type': account.account_type,
                                    'currency_type': account.currency_type.currency_type,
                                    'user': account.user.first_name,
                                    'amount': account.amount})
        return render(request, 'update_account.html', {'accountform': form, 'account_id': account.id,
                                                       'currency': currency, 'currencies': currencies,
                                                       'user': user, 'users': users})
    elif request.method == 'POST':
        obj = Accounts.objects.get(pk=pk)
        form = AccountForm(request.POST, instance=obj)
        form.save()
        obj.currency_type_id = request.POST.get('currency_type')
        obj.user_id = request.POST.get('user_id')
        obj.save()
        return redirect('settings')


def currency_list(request):
    c = Currency.objects.all()
    return render(request, 'currency_list.html', {'currencies': c})


def add_currency(request):

    if request.method == 'GET':
        return render(request, 'currency_add.html')
    elif request.method == 'POST':
        Currency.objects.create(currency_type=request.POST.get('currency'))
        currencies = Currency.objects.all()
        return render(request, 'currency_list.html', {'currencies': currencies})


def delete_currency(request, pk):
    c = Currency.objects.get(pk=pk)
    c.delete()
    currencies = Currency.objects.all()
    return render(request, 'currency_list.html', {'currencies': currencies})


def update_currency(request, pk):
    if request.method == 'GET':
        c = Currency.objects.get(pk=pk)
        return render(request, 'update_currency.html', {'curreny': c})
    elif request.method == 'POST':
        c = Currency.objects.get(pk=pk)
        c.currency_type=request.POST.get('currency')
        c.save()
        currencies = Currency.objects.all()
        return render(request, 'currency_list.html', {'currencies': currencies})