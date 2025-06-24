from django.urls import path
from . import views

name = 'account'

urlpatterns = [
    path('announcement/teacher/all/', views.view_all_announcement, name='view_all_announcement'),
    path('class/<int:class_id>/announcements/', views.view_class_announcement, name='view_class_announcement'),
    path('class/<int:class_id>/announcement/', views.create_announcement, name='create_announcement'),
    path('announcement/<int:announcement_id>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcement/<int:announcement_id>/delete/', views.delete_announcement, name='delete_announcement'),
    ]





