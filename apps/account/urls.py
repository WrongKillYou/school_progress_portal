from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import TeacherPasswordChangeForm
from . import views

name = 'account'

urlpatterns = [
    path('student/login/', views.student_login, name='student_login'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout, name='logout'),
    path('student/dashboard', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    path(
        "teacher/change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="account/teacher/change_password.html",
            success_url=reverse_lazy('teacher_password_changed'),  # <--- use name, not path!
            form_class=TeacherPasswordChangeForm
        ),
        name="teacher_change_password"
    ),
    path(
        "teacher/password-changed/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="account/teacher/password_changed.html"
        ),
        name="teacher_password_changed"
    ),
]
