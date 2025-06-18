from django.db import models
from account.models import Student
from classroom.models import Class


# Create your models here.
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')

    class Meta:
        unique_together = ('student', 'class_obj', 'date')

    def __str__(self):
        return f"{self.student} - {self.class_obj} on {self.date} [{self.status}]"
