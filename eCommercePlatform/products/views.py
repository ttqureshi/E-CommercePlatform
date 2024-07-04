from django.shortcuts import render
from .models import Product

# Create your views here.

def products_listing_view(request):
    products = Product.objects.all()
    return render(request, 'products/products_listing.html', {"products": products})