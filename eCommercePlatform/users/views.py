from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import UserRegisterForm
from django.contrib.auth import login

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("products:products-listing")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("products:products-listing")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})