from django.shortcuts import render, redirect
from accounts.models import *
from users.models import User
from django.contrib import messages
from e_branch.forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout
)


@login_required(login_url='login')
def index(request):
    return render(request, 'e-branch/_authorized.html')


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

    return render(request, 'e-branch/login.html', {
        'form': form
    })


def logout(request):
    auth_logout(request)
    return redirect('/')


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
def accounts (request):
    return render(request, 'e-branch/accounts.html')


@login_required(login_url='login')
def loans (request):
    return render(request, 'e-branch/loans.html')


@login_required(login_url='login')
def transactions (request):
    return render(request, 'e-branch/transactions.html')