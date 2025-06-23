from django.shortcuts import render, get_object_or_404
from account.models import Student
from django.contrib.auth.decorators import login_required
from config.decorators import role_required
from django.utils.timezone import now
from datetime import date
from django.http import JsonResponse
from attendance.models import Attendance
from django.core.serializers.json import DjangoJSONEncoder
import json
from classroom.models import Class


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
    if request.method == 'POST':
        lrn = request.POST.get('lrn')
        class_id = request.POST.get('class_id')  # optional if scanning in a known context

        try:
            student = Student.objects.get(lrn=lrn)
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Student not found'})

        class_obj = get_object_or_404(Class, id=class_id)

        today = date.today()
        attendance, created = Attendance.objects.get_or_create(
            student=student,
            class_obj=class_obj,
            date=today,
            defaults={'time_in': now().time(), 'status': 'incomplete'}
        )

        if not created:
            if attendance.time_out is None:
                attendance.time_out = now().time()
                attendance.status = 'present'
                attendance.save()
                return JsonResponse({'success': True, 'message': 'Time-out recorded'})
            else:
                return JsonResponse({'success': False, 'message': 'Attendance already complete'})
        else:
            # First scan recorded (time_in only)
            attendance.status = 'incomplete'
            attendance.save()
            return JsonResponse({'success': True, 'message': 'Time-in recorded'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# # # # # # # # # # # # # # # # # # # # # # # # #
@login_required
@role_required('teacher')
def view_student_attendance(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attendance_records = Attendance.objects.filter(student=student)

    attendance_data = [
        {
            'date': record.date.strftime('%Y-%m-%d'),  # Already a `date` object
            'status': record.status,
            'time_in': record.time_in.strftime('%H:%M:%S') if record.time_in else 'N/A',
            'time_out': record.time_out.strftime('%H:%M:%S') if record.time_out else 'N/A',
        }
        for record in attendance_records
    ]

    context = {
        'student': student,
        'attendance_json': json.dumps(attendance_data, cls=DjangoJSONEncoder)
    }
    return render(request, 'attendance/teacher/view_student_attendance.html', context)


# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def edit_student_attendance(request):
    # Edit a certain day of attendance of a student
    return None
