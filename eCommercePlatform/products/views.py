from django.shortcuts import render
from .models import Product

# Create your views here.


def products_listing_view(request):
    products = Product.objects.all()
    return render(request, "products/products_listing.html", {"products": products})


def product_detail_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, "products/product_detail.html", {"product": product})
