from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_listing_view, name='products-listing'),
]
