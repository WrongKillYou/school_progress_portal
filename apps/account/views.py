from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from account.models import Student, Teacher, User
from account.forms import StudentLoginForm, TeacherLoginForm
from django.contrib.auth.decorators import login_required
from config.decorators import role_required

# Create your views here.

# # # # # # # # # # # # #
# STUDENT 
# # # # # # # # # # # # #

def student_login(request):
    # Student login by scanning their QR Code
    if request.user.is_authenticated:
        return redirect('student_dashboard')  # redirect if already logged in

    form = StudentLoginForm(request.POST or None)
    if form.is_valid():
        lrn = form.cleaned_data['lrn']
        student = Student.objects.get(lrn=lrn)
        user = student.user
        login(request, user)
        return redirect('student_dashboard')
    return render(request, 'account/student/student_login.html', {'form': form})


@login_required
@role_required('student')
def student_dashboard(request):
    # Display of student dashboard, landing page after login
    return render(request, 'account/student/student_dashboard.html')


def focus_personal_info():
    # Upon clicking the name window, focus the avatar and basic info of the student
    return None


# # # # # # # # # # # # #
# TEACHER 
# # # # # # # # # # # # #

def teacher_login(request):
    # Teacher login by entering their credentials
    if request.user.is_authenticated:
        return redirect('teacher_dashboard')  # Redirect to teacher dashboard if already logged in

    form = TeacherLoginForm(request.POST or None)
    error = None

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:  # Ensure it's a teacher
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            error = "Invalid credentials or not a teacher account."

    return render(request, 'account/teacher/teacher_login.html', {
        'form': form,
        'error': error
    })


def teacher_dashboard(request):
    # Display of teacher dashboard, landing page after login
    return render(request, 'account/teacher/teacher_dashboard.html')


def logout(request):
    # Logout
    django_logout(request)
    return redirect('student_login')



