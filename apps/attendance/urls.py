from django.urls import path
from . import views

name = 'account'

urlpatterns = [
    path('teacher/<int:student_id>/attendance/', views.view_student_attendance, name='view_student_attendance'),
    ]
