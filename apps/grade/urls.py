from django.urls import path
from . import views

name = 'account'

urlpatterns = [
    path('class/<int:class_id>/upload-grade/', views.upload_grade, name='upload_grade'),
    ]
