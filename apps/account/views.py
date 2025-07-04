from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from datetime import date
import json

from account.models import Student, Teacher, User
from account.forms import StudentLoginForm, TeacherLoginForm

from django.contrib.auth.decorators import login_required
from config.decorators import role_required

from account.models import Student
from announcement.models import Announcement
from classroom.models import Class, Enrollment
from badge.models import BadgeShard
from grade.models import GradeItem, FinalGrade

from account.services import (
    get_enrolled_classes,
    get_recent_announcements,
    build_grade_starplot,
    get_monthly_attendance,
    badge_breakdown,
)



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


@login_required
@role_required("student")
def student_dashboard(request):
    student = request.user.student_profile

    classes           = get_enrolled_classes(student)
    announcements     = get_recent_announcements(classes)
    labels, values    = build_grade_starplot(student, classes)
    attendance_data   = get_monthly_attendance(student)
    badge_ctx         = badge_breakdown(student)

    # ⭐ Build detail = {subject: {"1": {...}, "2": {...}}}
    detail = {}
    finals = (
        FinalGrade.objects
        .filter(student=student)
        .select_related("class_obj")
    )

    for fg in finals:
        # ensure final_grade is populated
        if fg.final_grade is None:
            fg.compute_final_grade()

        subj = fg.class_obj.subject
        qtr  = str(fg.quarter)          # JSON keys must be strings

        detail.setdefault(subj, {})[qtr] = {
            "final": fg.final_grade,
            "components": list(
                GradeItem.objects
                .filter(
                    student=student,
                    class_obj=fg.class_obj,
                    quarter=fg.quarter
                )
                .values("component", "score", "highest_possible_score")
            )
        }

    context = {
        "student": student,
        "classes": classes,
        "announcements": announcements,
        "grade_labels": labels,
        "grade_values": values,
        "attendance_data": attendance_data,
        "starplot_detail_json": json.dumps(detail),
        **badge_ctx,
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



