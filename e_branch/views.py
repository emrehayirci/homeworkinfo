from django.shortcuts import render, redirect
from accounts.models import *
from users.models import User
from django.contrib import messages
from e_branch.forms import RegistrationForm, TransactionCreationForm, LoginForm, AccountCreationForm, LoanCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout
)


@login_required(login_url='login')
def index(request):
    return redirect('accounts')


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            auth_login(request, form.user)
            messages.info(
                request,
                'Giriş yaptınız.'
            )
            return redirect('index')

    return render(request, 'e-branch/login.html', {
        'form': form
    })


def logout(request):
    auth_logout(request)
    return redirect('index')


def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

    if form.is_valid():
        form.save()

        messages.info(
            request,
            'Kayıt başarılı. Şimdi login olabilirsiniz.'
        )

        return redirect('login')

    return render(request, 'e-branch/register.html', {
        'form': form,
    })


@login_required(login_url='login')
def accounts(request):
    useraccounts = Accounts.objects.filter(user=request.user)
    form = AccountCreationForm()
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            form.save(request.user)

            messages.info(
                request,
                'New Account Created!'
            )
    return render(request, 'e-branch/accounts.html', {'accounts': useraccounts, 'form': form})


@login_required(login_url='login')
def loans(request):
    form = LoanCreationForm()
    unpaid_debt = LoanAccountPayment.objects.filter(account__user=request.user.id, is_active=True, is_paid=False)
    currentloans = Loan.objects.filter(account__user=request.user.id)
    if request.method == 'POST':
        form = LoanCreationForm(request.POST, request=request)

        if form.is_valid():
            messages.info(
                request,
                'New Loan Created!'
            )
    return render(request, 'e-branch/loans.html', {'loans': currentloans, 'form': form, 'unpaid': unpaid_debt})


@login_required(login_url='login')
def transactions(request):
    form = TransactionCreationForm(request=request)
    transaction_history = Transaction.objects.filter(sourceaccount__user=request.user, is_done=True)
    if request.method == 'POST':
        form = TransactionCreationForm(request.POST, request=request)
        if form.is_valid():
            messages.info(
                request,
                'New Transactions Created!'
            )
    return render(request, 'e-branch/transactions.html', {'form': form, 'transactions': transaction_history})