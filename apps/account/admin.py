from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django import forms
from .models import User, Student, Teacher

# ========================================
# Custom Forms for Creating Student & Teacher with User
# ========================================

class StudentCreationForm(forms.ModelForm):
    # User fields
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Student
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # Editing: fill user fields from related user
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['password'].help_text = "Leave blank if you don't want to change the password."

        # Field order
        user_fields = ['username', 'password', 'email', 'first_name', 'last_name']
        student_fields = [f for f in self.fields if f not in user_fields]
        self.order_fields(user_fields + student_fields)

    def save(self, commit=True):
        student = super().save(commit=False)

        if not student.user_id:
            # Create new user
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='student'
            )
        else:
            # Update existing user
            user = student.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()

        student.user = user
        if commit:
            student.save()
        return student




class TeacherCreationForm(forms.ModelForm):
    # User fields
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Teacher
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # Editing: fill user fields from related user
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['password'].help_text = "Leave blank if you don't want to change the password."

        # Field order
        user_fields = ['username', 'password', 'email', 'first_name', 'last_name']
        teacher_fields = [f for f in self.fields if f not in user_fields]
        self.order_fields(user_fields + teacher_fields)

    def save(self, commit=True):
        teacher = super().save(commit=False)

        if not teacher.user_id:
            # Create new user
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='student'
            )
        else:
            # Update existing user
            user = teacher.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()

        teacher.user = user
        if commit:
            teacher.save()
        return teacher


# ========================================
# Custom Admin Classes
# ========================================

class StudentAdmin(admin.ModelAdmin):
    form = StudentCreationForm
    list_display = ('get_full_name', 'lrn', 'level', 'section')
    search_fields = ('user__username', 'lrn', 'user__first_name', 'user__last_name')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Student Name'


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherCreationForm
    list_display = ('get_full_name', 'license_number', 'department')
    search_fields = ('user__username', 'license_number', 'user__first_name', 'user__last_name')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Teacher Name'

# ========================================
# Register Models
# ========================================

# Optional: hide User, Group, and Permission from admin
for model in [User, Group, Permission]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
