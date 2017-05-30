from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm
from .models import Accounts, Currency, Transaction, ACCOUNT_TYPE_CHOICES, LoanAccountPayment, Loan
from IPython import embed
from users.models import User
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
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
        currencies = Currency.objects.all()

        return render(request, 'create_account.html', {'accountform': form, 'users': users, 'currencies': currencies,
                                                       'choices': ACCOUNT_TYPE_CHOICES})
    elif request.method == 'POST':
        currency = Currency.objects.filter(pk=request.POST.get('currency_type'))
        if len(currency) > 0:
            currency = currency[0]
        else:
            currency = Currency.objects.first()
        Accounts.objects.create(iban=request.POST.get('iban'), account_type=request.POST.get('account_type'),
                                user_id=request.POST.get('user_id'), currency_type=currency,
                                amount=request.POST.get('amount'))
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
        form.instance.account_type = request.POST.get('account_type')
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
        c.currency_type = request.POST.get('currency')
        c.save()
        currencies = Currency.objects.all()
        return render(request, 'currency_list.html', {'currencies': currencies})


def transactions_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions/transactions.html', {'transactions': transactions})


def cancel_transaction(request, pk):
    if request.user.is_staff is True:
        transaction = get_object_or_404(Transaction, pk=pk)
        if transaction.cancel_validate_transaction():
            transaction.cancel_transaction()
    return redirect('transactions_a')


def delete_transaction(request, pk=None):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('transactions_a')


def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'loans/loans.html', {'loans': loans})


def loan_detail(request, pk=None):
    loan = get_object_or_404(Loan, pk=pk)
    loans_payments = LoanAccountPayment.objects.filter(loan=loan)
    return render(request, 'loans/loan_detail.html', {'loan': loan, 'loans_payments': loans_payments})


def pay(request, pk=None):
    loan_payment = get_object_or_404(LoanAccountPayment, pk=pk)
    if loan_payment.is_paid is True:
        LoanAccountPayment.objects.filter(pk=pk).update(is_paid=False)
    else:
        LoanAccountPayment.objects.filter(pk=pk).update(is_paid=True)
    return redirect('loan_detail', pk=loan_payment.loan.id)


@api_view(['POST', 'GET'])
def api_transaction(request):
    s_a = get_object_or_404(Accounts, iban=request.data.get('source_account'))
    d_a = get_object_or_404(Accounts, iban=request.data.get('destination_account'))
    amount = int(request.data.get('amount'))
    t = Transaction.objects.create(description=request.data.get('description'), amount=amount,
                                   sourceaccount=s_a, destinationaccount=d_a, currency_type=s_a.currency_type)
    if t.validate_transaction():
        t = t.make_transaction()
        return Response({'IsSuccess': True, 'bank_receiptID': t.id})
    else:
        return Response({'IsSuccess': False, 'context': 'Credit is not enough'})


@api_view(['GET'])
def query_receipt(request, pk):
    t = Transaction.objects.filter(pk=pk)
    if len(t) > 0:
        return Response({'IsExist': True})
    else:
        return Response({'IsExist': False})

