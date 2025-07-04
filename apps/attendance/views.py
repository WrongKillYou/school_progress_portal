from django.shortcuts import render, get_object_or_404

import json
from django.utils.timezone import now
from datetime import date, datetime
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from account.models import Student
from classroom.models import Class, Enrollment
from attendance.models import Attendance

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
    teacher = request.user.teacher_profile
    classes = Class.objects.filter(teacher=teacher)
    return render(request, 'attendance/teacher/scan_attendance.html', {'classes': classes})

# # # # # # # # # # # # # # # # # # # # # # # # #


@login_required
@role_required('teacher')
def register_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lrn = data.get('lrn')
            class_id = data.get('class_id')

            if not class_id:
                return JsonResponse({'status': 'danger', 'message': 'Class not selected'})

            student = Student.objects.get(lrn=lrn)
            class_obj = Class.objects.get(id=class_id)

            # Check enrollment
            if not Enrollment.objects.filter(student=student, class_obj=class_obj).exists():
                return JsonResponse({'status': 'danger', 'message': f"{student.user.get_full_name()} is not enrolled in this class."})

            # Proceed with attendance logic
            today = date.today()
            now = datetime.now().time()
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                class_obj=class_obj,
                date=today,
                defaults={'time_in': now}
            )

            if not created:
                if not attendance.time_out:
                    attendance.time_out = now
                    attendance.save()
                    return JsonResponse({'status': 'success', 'message': f'Time-out for {student.user.get_full_name()} complete.'})
                else:
                    return JsonResponse({'status': 'info', 'message': 'Both time-in and time-out already recorded.'})
            else:
                return JsonResponse({'status': 'success', 'message': f'Time-in for {student.user.get_full_name()} complete.'})

        except Student.DoesNotExist:
            return JsonResponse({'status': 'danger', 'message': 'Invalid or unknown LRN.'})
        except Exception as e:
            return JsonResponse({'status': 'danger', 'message': str(e)})


@login_required
@role_required('teacher')
def view_student_attendance(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Get the specific class where this student is enrolled — adjust as needed
    enrollment = Enrollment.objects.filter(student=student).first()
    class_obj = enrollment.class_obj if enrollment else None

    attendance_records = Attendance.objects.filter(student=student)

    attendance_data = [
        {
            'date': record.date.strftime('%Y-%m-%d'),
            'status': record.status,
            'time_in': record.time_in.strftime('%H:%M:%S') if record.time_in else 'N/A',
            'time_out': record.time_out.strftime('%H:%M:%S') if record.time_out else 'N/A',
        }
        for record in attendance_records
    ]

    context = {
        'student': student,
        'class_obj': class_obj,
        'attendance_json': json.dumps(attendance_data, cls=DjangoJSONEncoder),
    }

    return render(request, 'attendance/teacher/view_student_attendance.html', context)



# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def edit_student_attendance(request):
    # Edit a certain day of attendance of a student
    return None
