from django.urls import path
from . import views

app_name= "Dashboard"

urlpatterns = [
    path("", views.Dashboard, name="index"),
]