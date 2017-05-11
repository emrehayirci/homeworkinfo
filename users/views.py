from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .forms import UserForm
from IPython import embed

# Create your views here.

def auth(request):
    if request.user.is_authenticated() is True:
        return redirect('settings')
    form = UserForm(request.POST or None)
    if form.is_valid():
        sign_up = form.save(commit=False)
        sign_up.password = make_password(form.cleaned_data['password'])
        sign_up.save()
        login(request, sign_up)
        return redirect('settings')
    return render(request, 'login.html',)


def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('settings')

    return redirect('/users/auth/')

def logut_user(request):
    logout(request)
    return redirect('auth')