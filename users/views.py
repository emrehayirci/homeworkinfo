from django.shortcuts import render
from django.http import HttpResponse
from IPython import embed

# Create your views here.

def auth(request):
    return render(request, 'login.html',)

def login(request):
    return HttpResponse('')