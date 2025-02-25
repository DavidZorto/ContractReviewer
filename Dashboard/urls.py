from django.urls import path
from . import views

app_name= "Dashboard"

urlpatterns = [
    path("", views.Dashboard, name="index"),
    path('home/', views.Dashboard_home, name='dashboard_home'),
    path('briefcases/', views.Briefcases, name='briefcases'),
    path('documents/', views.Documents, name='documents'),
    path('processing-jobs/', views.Processing_jobs, name='processing_jobs'),
    path('answers/', views.Answers, name='answers'),


    path('briefcases/delete/<uuid:id>/', views.delete_briefcase, name='delete_briefcase'),
    path('briefcases/create/', views.create_briefcase, name='create_briefcase'),

]