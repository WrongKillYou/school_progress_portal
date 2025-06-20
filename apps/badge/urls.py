from django.urls import path
from . import views

name = 'account'

urlpatterns = [
    path('give/<int:student_id>/<int:class_id>/', views.give_badge, name='give_badge'),
    path('student/<int:student_id>/class/<int:class_id>/badges/', views.view_student_badge, name='view_student_badge'),
    ]
