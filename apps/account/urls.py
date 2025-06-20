from django.urls import path
from . import views

name = 'account'

urlpatterns = [
    path('student/login/', views.student_login, name='student_login'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout, name='logout'),
    path('student/dashboard', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    ]
