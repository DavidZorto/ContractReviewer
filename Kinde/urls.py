from django.urls import path

from . import views

app_name="Kinde"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("callback/", views.callback, name="callback"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
]
