from django.urls import path

from . import views

app_name = 'users' # designates that these urls are inside the users app

urlpatterns = [
    path('register/', views.register_view, name='register'),
    ]