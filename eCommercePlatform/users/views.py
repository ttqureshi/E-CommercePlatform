from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm
from products.models import Product
from .models import Cart, CartItem

# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            cart = Cart(user=request.user)
            cart.save()
            return redirect("products:products-listing")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("products:products-listing")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        redirect("products:products-listing")

@login_required(login_url="/login")
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.cartitem_set.all()
    total_price = sum(item.quantity * item.product.price for item in items)

    return render(request, 'users/cart.html', {"cart": cart, "total_price": total_price})


@login_required(login_url="/login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    in_stock = product.stock > 0

    if in_stock:
        cart = Cart.objects.get(user=request.user)
        cart_item, is_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not is_created:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1
    
    return redirect("users:cart")


@login_required(login_url="/login")
def update_cart_item(request, product_id):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.get(product_id=product_id)
        product = Product.objects.get(id=product_id)
        stock_left = product.stock
        quantity = int(request.POST.get('quantity'))
        if quantity <= stock_left:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            messages.warning(request, f"Only {stock_left} {product.name} left in stock.")
        return redirect("users:cart")
    return redirect("users:cart")


@login_required(login_url="/login")
def remove_item(request, product_id):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.get(product_id=product_id)
        cart_item.delete()
        return redirect("users:cart")
