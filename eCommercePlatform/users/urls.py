from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"  # designates that these urls are inside the users app

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="products:products-listing"),
        name="logout",
    ),
]
