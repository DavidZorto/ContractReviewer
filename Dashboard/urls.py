from django.urls import path
from . import views

app_name= "Dashboard"

urlpatterns = [
    path("", views.Dashboard, name="index"),
    path('Dashboard/home/', views.Dashboard_home, name='dashboard_home'),
    path('Dashboard/briefcases/', views.Briefcases, name='briefcases'),
    path('Dashboard/documents/', views.Documents, name='documents'),
    path('Dashboard/processing-jobs/', views.Processing_jobs, name='processing_jobs'),
    path('Dashboard/answers/', views.Answers, name='answers'),
]