from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .forms import UserForm, AddressForm
from users.models import User, Address
from accounts.models import Accounts
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
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('settings')

    return redirect('/users/auth/')


def logut_user(request):
    logout(request)
    return redirect('auth')


def users_list(request):
    users = User.objects.all()
    for user in users:
        total = 0
        accounts = Accounts.objects.filter(user_id=user.id)
        if len(accounts) > 0:
            for account in accounts:
                total += account.amount
            user.total_credit = total
            user.accounts = accounts
    return render(request, 'users/users.html', {'users': users})


def create_user(request):
    if request.method == 'GET':
        return render(request, 'users/create_user_form.html')
    elif request.method == 'POST':
        user = User.objects.create_user(email=request.POST.get('email'), password=request.POST.get('password'),
                                        last_name=request.POST.get('last_name'),
                                        first_name=request.POST.get('first_name'),
                                        phone_no=request.POST.get('phone_no'))
        Address.objects.create(street=request.POST.get('street'), district=request.POST.get('district'),
                               zipcode=request.POST.get('zipcode'), city=request.POST.get('city'),
                               no=request.POST.get('no'), user=user)
        embed()
        return redirect('users')


def edit_user(request, pk):
    if request.method == 'GET':
        # user = User.objects.filter(pk=pk)
        user = get_object_or_404(User, pk=pk)
        # address = Address.objects.filter(user_id=pk)
        address = get_object_or_404(Address, user_id=user.id)
        # if len(user) < 1 and address < 1:
        #     return redirect('users')
        # else:
        #     user = user[0]
        #     address = address[0]
        return render(request, 'users/edit_user.html', {'address': address, 'user': user})
    elif request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        address = get_object_or_404(Address, user_id=user.id)
        user_form = UserForm(request.POST, instance=user)
        address_form = AddressForm(request.POST, instance=address)
        if address_form.is_valid() is True and user_form.is_valid() is True:
            address_form.save()
            u = User.objects.get(pk=pk)
            if u.password != user.password:
                user_form.instance.password = make_password(user.password)
            user_form.save()
        return redirect('users')


