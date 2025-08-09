from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('create/', views.resume_create, name='resume_create'),
    path('resumes/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('resumes/<int:resume_id>/pdf/', views.resume_pdf, name='resume_pdf'),
    path('resumes/<int:resume_id>/copy/', views.resume_copy, name='resume_copy'),
]