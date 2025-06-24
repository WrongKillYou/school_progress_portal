from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from config.decorators import role_required

from account.models import Student
from classroom.models import Class
from badge.models import BadgeShard
from badge.forms import BadgeShardForm



# Create your views here.

# # # # # # # # # # # # #
# STUDENT 
# # # # # # # # # # # # #

def focus_badge():
    # Upon clicking the badge window, focus the badge collection in the screen
    return None


def view_badge():
    # View the badge and shards, together with the basic info
    return None



# # # # # # # # # # # # #
# TEACHER 
# # # # # # # # # # # # #


@login_required
@role_required('teacher')
def view_student_badge(request, student_id, class_id):
    # View the badge collection of an individual student
    student = get_object_or_404(Student, id=student_id)
    class_obj = get_object_or_404(Class, id=class_id)

    merit_shards = BadgeShard.objects.filter(student=student, class_obj=class_obj, type='merit')
    demerit_shards = BadgeShard.objects.filter(student=student, class_obj=class_obj, type='demerit')

    merit_count = merit_shards.count()
    demerit_count = demerit_shards.count()

    context = {
        'student': student,
        'class_obj': class_obj,
        'merit_shards': merit_shards,
        'demerit_shards': demerit_shards,
        'merit_badges': merit_count // 5,
        'demerit_badges': demerit_count // 4,
        'empty_merit': range(5 - (merit_count % 5) if merit_count % 5 < 5 else 0),
        'empty_demerit': range(4 - (demerit_count % 4) if demerit_count % 4 < 4 else 0),
    }

    return render(request, 'badge/teacher/view_student_badge.html', context)

# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def give_badge(request, student_id, class_id):
    # Give a shard or badge to the student, stating the reason
    student = get_object_or_404(Student, id=student_id)
    class_obj = get_object_or_404(Class, id=class_id)
    teacher = request.user.teacher_profile

    if request.method == 'POST':
        form = BadgeShardForm(request.POST)
        if form.is_valid():
            shard = form.save(commit=False)
            shard.student = student
            shard.class_obj = class_obj
            shard.teacher = teacher
            shard.save()
            return redirect('view_class_list', class_id=class_id)
    else:
        form = BadgeShardForm()

    return render(request, 'badge/teacher/give_badge.html', {
        'form': form,
        'student': student,
        'class_obj': class_obj,
    })

# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def delete_badge(request, shard_id):
     # Delete a shard or badge of the student
    shard = get_object_or_404(BadgeShard, id=shard_id)

    if request.method == "POST":
        shard.delete()
        messages.success(request, f"{shard.type.title()} shard deleted successfully.")
        return redirect("view_student_badge", student_id=shard.student.id, class_id=shard.class_obj.id)

    return HttpResponseForbidden("Only POST method is allowed.")


