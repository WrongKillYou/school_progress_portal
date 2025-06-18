from django.db import models
from account.models import Student, Teacher
from classroom.models import Class

class BadgeShard(models.Model):
    TYPE_CHOICES = [
        ('merit', 'Merit'),
        ('demerit', 'Demerit'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='shards')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    reason = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.title()} shard for {self.student} in {self.class_obj}"
