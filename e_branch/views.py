from django.shortcuts import render
from accounts import models
# Create your views here.
def index (request):

    return render(request, 'e-branch/_authorized.html')

def login (request):
    return render(request, 'e-branch/login.html')

def register (request):
    return render(request, 'e-branch/register')

def accounts (request):
    return render(request, 'e-branch/accounts')

def loans (request):
    return render(request, 'e-branch/loans')
