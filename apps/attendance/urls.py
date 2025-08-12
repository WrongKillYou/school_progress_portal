from django.urls import path
from . import views

name = 'account'

urlpatterns = [
    path('teacher/<int:student_id>/attendance/', views.view_student_attendance, name='view_student_attendance'),
    path('teacher/scan/', views.scan_attendance, name='scan_attendance'),
    path('teacher/scan/register/', views.register_attendance, name='register_attendance'),
    path("start-class/", views.start_class, name="start_class"),
    ]
