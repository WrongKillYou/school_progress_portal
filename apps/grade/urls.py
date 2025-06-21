from django.urls import path
from . import views

name = 'account'

urlpatterns = [
    path('upload/<int:class_id>/', views.upload_grade, name='upload_grade'),
    path('download-template/<int:class_id>/', views.download_file, name='download_file'),
    path('teacher/grade/<int:student_id>/<int:class_id>/', views.view_grade, name='view_grade'),
    path('teacher/grade/<int:student_id>/<int:class_id>/<int:quarter>/', views.view_grade, name='view_grade'),



    ]
