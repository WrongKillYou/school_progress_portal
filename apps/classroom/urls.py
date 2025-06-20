from django.urls import path
from . import views

name = 'classroom'

urlpatterns = [
    path('teacher/class/', views.view_handled_class, name='view_handled_class'),
    path('teacher/class/<int:class_id>/students/', views.view_class_list, name='view_class_list'),
    ]
