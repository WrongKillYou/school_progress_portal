from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as django_logout
from datetime import date
import json
from django.core.serializers.json import DjangoJSONEncoder


from account.models import Student, Teacher, User
from account.forms import StudentLoginForm, TeacherLoginForm

from django.contrib.auth.decorators import login_required
from config.decorators import role_required

from account.models import Student
from announcement.models import Announcement
from classroom.models import Class, Enrollment
from badge.models import BadgeShard
from grade.models import GradeItem, FinalGrade

from account.services import *



# Create your views here.

# # # # # # # # # # # # #
# STUDENT 
# # # # # # # # # # # # #

def student_login(request):
    # Student login by scanning their QR Code (but text LRN for now)
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





# student_dashboard/views.py (or wherever you prepare modal data)








@login_required
@role_required("student")
def student_dashboard(request):
    student = request.user.student_profile
    classes           = get_enrolled_classes(student)

    announcements     = get_recent_announcements(classes)

    starplot_detail   = build_grade_starplot_detail(student, classes)
    starplot_json, grade_labels = build_all_quarters_starplot(student)
    labels = list(starplot_detail.keys())
    values = [starplot_detail[subj].get("1", {}).get("final", 0) for subj in labels]

    attendance_records = Attendance.objects.filter(student=student)
    attendance_data = [
        {
            'date': record.date.strftime('%Y-%m-%d'),
            'status': record.status.lower(),  # ensure lowercase for CSS match
            'time_in': record.time_in.strftime('%H:%M:%S') if record.time_in else '—',
            'time_out': record.time_out.strftime('%H:%M:%S') if record.time_out else '—',
        }
        for record in attendance_records
    ]

    badge_ctx         = badge_breakdown(student)
    merit_shards = BadgeShard.objects.filter(student=student, type="merit")
    demerit_shards = BadgeShard.objects.filter(student=student, type="demerit")

    



    context = {
        "student": student,
        "classes": classes,
        "announcements": announcements,
        "grade_labels": labels,
        "grade_values": values,
        "attendance_json": json.dumps(attendance_data, cls=DjangoJSONEncoder),
        "starplot_detail_json": json.dumps(starplot_detail),
        **badge_ctx,
        "merit_shards": merit_shards,
        "demerit_shards": demerit_shards,
        "all_quarters_starplot_json":starplot_json,
    }
    return render(
        request,
        "account/student/student_dashboard.html",
        context
    )

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

@login_required
@role_required('teacher')
def teacher_dashboard(request):
    # Display of teacher dashboard, landing page after login
    teacher = request.user.teacher_profile

    handled_classes = Class.objects.filter(teacher=teacher)
    total_classes = handled_classes.count()
    total_students = Enrollment.objects.filter(class_obj__in=handled_classes).values('student').distinct().count()
    total_announcements = Announcement.objects.filter(teacher=teacher).count()
    total_merit = BadgeShard.objects.filter(teacher=teacher, type='merit').count()
    total_demerit = BadgeShard.objects.filter(teacher=teacher, type='demerit').count()

    context = {
        'teacher': teacher,
        'total_classes': total_classes,
        'total_students': total_students,
        'total_announcements': total_announcements,
        'total_merit': total_merit,
        'total_demerit': total_demerit,
    }

    return render(request, 'account/teacher/teacher_dashboard.html', context)


def logout(request):
    # Logout
    django_logout(request)
    return redirect('student_login')



