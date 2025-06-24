from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from config.decorators import role_required

from classroom.models import Class
from announcement.forms import AnnouncementForm
from announcement.models import Announcement


# Create your views here.

# # # # # # # # # # # # #
# STUDENT 
# # # # # # # # # # # # #

def focus_announcement():
    # Upon clicking the announcement window, focus the lists of announcements from every class
    return None

# # # # # # # # # # # # # # # # # # # # # # # # #

def view_announcement():
    # View an individual announcement
    return None



# # # # # # # # # # # # #
# TEACHER 
# # # # # # # # # # # # #

@login_required
@role_required('teacher')
def view_class_announcement(request, class_id):
    # View the lists of announcement from a class
    class_obj = get_object_or_404(Class, id=class_id)
    announcements = Announcement.objects.filter(class_obj=class_obj).order_by('-date_posted')
    
    return render(request, 'announcement/teacher/view_class_announcement.html', {
        'class_obj': class_obj,
        'announcements': announcements
    })


# # # # # # # # # # # # # # # # # # # # # # # # #


def view_all_announcement(request):
    # View all announcements created by the teacher; filter process added
    teacher = request.user.teacher_profile
    selected_class_id = request.GET.get('class_id')

    # All classes this teacher handles
    teacher_classes = Class.objects.filter(teacher=teacher)

    # Filter announcements by class if class_id is provided
    if selected_class_id and selected_class_id != 'all':
        announcements = Announcement.objects.filter(teacher=teacher, class_obj__id=selected_class_id).order_by('-date_posted')
    else:
        announcements = Announcement.objects.filter(teacher=teacher).order_by('-date_posted')

    return render(request, 'announcement/teacher/view_all_announcement.html', {
        'announcements': announcements,
        'teacher_classes': teacher_classes,
        'selected_class_id': selected_class_id or 'all',
    })





@login_required
@role_required('teacher')
def create_announcement(request, class_id):
    # Create an announcement for a certain class
    class_obj = get_object_or_404(Class, id=class_id)
    teacher = request.user.teacher_profile

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.teacher = teacher
            announcement.class_obj = class_obj
            announcement.save()
            return redirect('view_class_list', class_id=class_obj.id)
    else:
        form = AnnouncementForm()

    return render(request, 'announcement/teacher/create_announcement.html', {
        'form': form,
        'class_obj': class_obj
    })

# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def edit_announcement(request, announcement_id):
    # Edit an announcement for a certain class
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # Only the teacher who posted it can edit
    if request.user != announcement.teacher.user:
        return redirect('view_class_announcement', class_id=announcement.class_obj.id)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('view_class_announcement', class_id=announcement.class_obj.id)
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'announcement/teacher/edit_announcement.html', {
        'form': form,
        'announcement': announcement,
    })


# # # # # # # # # # # # # # # # # # # # # # # # #

@login_required
@role_required('teacher')
def delete_announcement(request, announcement_id):
    # Delete an announcement for a certain class
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # Only the teacher who posted it can delete
    if request.user == announcement.teacher.user:
        class_id = announcement.class_obj.id
        announcement.delete()
        return redirect('view_class_announcement', class_id=class_id)

    return redirect('view_class_announcement', class_id=announcement.class_obj.id)
