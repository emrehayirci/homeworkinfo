from django.shortcuts import render
from accounts.models import *
from users.models import User
from django.contrib.auth.decorators import login_required

#from django.contrib.auth import
# Create your views here.
@login_required(login_url='login')
def index (request):

    return render(request, 'e-branch/_authorized.html')

def login (request):
    return render(request, 'e-branch/login.html')

def register (request):
    return render(request, 'e-branch/register.html')

@login_required(login_url='login')
def accounts (request):
    return render(request, 'e-branch/accounts.html')

@login_required(login_url='login')
def loans (request):
    return render(request, 'e-branch/loans.html')

@login_required(login_url='login')
def transactions (request):
    return render(request, 'e-branch/transactions.html')