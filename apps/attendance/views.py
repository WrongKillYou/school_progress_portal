from django.shortcuts import render, get_object_or_404
from account.models import Student
from django.contrib.auth.decorators import login_required
from config.decorators import role_required

# Create your views here.

# # # # # # # # # # # # #
# STUDENT 
# # # # # # # # # # # # #

def focus_attendance(request):
    # Upon clicking the calendar window, focus the calendar attendance 
    return None


# # # # # # # # # # # # #
# TEACHER 
# # # # # # # # # # # # #


@login_required
@role_required('teacher')
def scan_attendance(request):
    # Scan the student's QR code to register attendance; first scan (time-in) and second scan (timeout)
    return None

# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def view_student_attendance(request, student_id):
    # View the individual student attendance calendar
    student = get_object_or_404(Student, id=student_id)

    # For now, just display student info. Later you can show attendance or events.
    context = {
        'student': student
    }
    return render(request, 'attendance/teacher/view_student_attendance.html', context)

# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def edit_student_attendance(request):
    # Edit a certain day of attendance of a student
    return None
