from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    middle_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}".strip()
        return f"{full_name} ({self.role})"

    def is_student(self):
        return self.role == 'student'

    def is_teacher(self):
        return self.role == 'teacher'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    lrn = models.CharField("Learner Reference Number", max_length=50, unique=True)
    level = models.CharField("Grade Level", max_length=10)
    section = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Parent/guardian info
    parent_name = models.CharField(max_length=255)
    parent_email = models.EmailField()
    parent_contact = models.CharField(max_length=50)

    # Optional info
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.level}-{self.section}"


# ==========================
# Teacher Model
# ==========================
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    license_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=255)

    # Optional profile info
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True)
    birth_date = models.DateField(null=True, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_number = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.department})"
