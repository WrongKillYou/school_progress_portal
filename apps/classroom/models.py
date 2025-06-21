from django.db import models
from account.models import Student, Teacher

class Class(models.Model):
    class_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_name} - {self.subject}"
    
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"  # Correct plural!
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')

    class Meta:
        unique_together = ('student', 'class_obj')

    def __str__(self):
        return f"{self.student} enrolled in {self.class_obj}"