from django.db import models
from account.models import Teacher
from classroom.models import Class


# ==========================
# Announcement Model
# ==========================
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='announcements')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='announcements')

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f"{self.title} - {self.class_obj.class_name} by {self.teacher.user.get_full_name()}"