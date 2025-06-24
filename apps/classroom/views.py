from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from config.decorators import role_required

from account.models import Teacher
from .models import Class, Enrollment


# Create your views here.

# # # # # # # # # # # # #
# STUDENT 
# # # # # # # # # # # # #





# # # # # # # # # # # # #
# TEACHER 
# # # # # # # # # # # # #

@login_required
@role_required('teacher')
def view_handled_class(request):
    # View the list of handled class by the teacher
    user = request.user
    try:
        teacher = user.teacher_profile  # This assumes OneToOneField from Teacher to User with related_name='teacher'
    except Teacher.DoesNotExist:
        return render(request, 'error.html', {'message': 'Teacher not found.'})

    classes = Class.objects.filter(teacher=teacher)
    return render(request, 'classroom/teacher/view_handled_class.html', {
        'teacher': teacher,
        'classes': classes
    })

# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def view_class_list(request, class_id):
    # View the list of students enrolled in the class, embedded with some possible actions

    class_obj = get_object_or_404(Class, id=class_id)
    
    enrollments = Enrollment.objects.filter(class_obj=class_obj).select_related('student__user')

    context = {
        'class_obj': class_obj,
        'enrollments': enrollments
    }
    return render(request, 'classroom/teacher/view_class_list.html', context)

