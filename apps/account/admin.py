from django.contrib import admin
from .models import User, Student, Teacher
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'role', 'is_active', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)

# Password: teacherpass12345