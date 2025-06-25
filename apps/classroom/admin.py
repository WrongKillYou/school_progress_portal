from django.contrib import admin
from django import forms
from account.models import Student, Teacher
from classroom.models import Class, Enrollment
from grade.models import GradingScheme

# ============================================
# Custom Form for Unified Creation
# ============================================

class ClassWithExtrasForm(forms.ModelForm):
    # GradingScheme fields
    written_work_weight = forms.FloatField(initial=0.4)
    performance_task_weight = forms.FloatField(initial=0.4)
    quarterly_assessment_weight = forms.FloatField(initial=0.2)

    # Enrollment selection
    enrolled_students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("Students", is_stacked=False)
    )

    class Meta:
        model = Class
        fields = ['class_name', 'subject', 'teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing existing Class, preselect currently enrolled students
        if self.instance.pk:
            self.fields['enrolled_students'].initial = Student.objects.filter(
                enrollment__class_obj=self.instance
            )

    def save(self, commit=True):
    # Always get the instance but don’t rely on `commit`
        class_instance = super().save(commit=False)   # <<< unsaved
        class_instance.save()                         # <<< ensure it has a PK

    # -------------------------
    #  now it’s safe to proceed
    # -------------------------
        GradingScheme.objects.update_or_create(
            class_obj=class_instance,
            defaults={
                'written_work_weight': self.cleaned_data['written_work_weight'],
                'performance_task_weight': self.cleaned_data['performance_task_weight'],
                'quarterly_assessment_weight': self.cleaned_data['quarterly_assessment_weight'],
            }
        )

        selected_students = set(self.cleaned_data.get('enrolled_students', []))
        current_enrollments = set(Enrollment.objects.filter(class_obj=class_instance))
        current_students = {e.student for e in current_enrollments}

        # Remove and add enrollments
        for enrollment in current_enrollments:
            if enrollment.student not in selected_students:
                enrollment.delete()

        for student in selected_students - current_students:
            Enrollment.objects.create(student=student, class_obj=class_instance)

        return class_instance


# ============================================
# Admin Class
# ============================================

class ClassAdmin(admin.ModelAdmin):
    form = ClassWithExtrasForm
    list_display = ('class_name', 'subject', 'teacher')
    search_fields = ('class_name', 'subject', 'teacher__user__last_name')

    # Optional: separate out form layout
    fieldsets = (
        ('Class Information', {
            'fields': ('class_name', 'subject', 'teacher')
        }),
        ('Grading Scheme', {
            'fields': ('written_work_weight', 'performance_task_weight', 'quarterly_assessment_weight')
        }),
        ('Enroll Students', {
            'fields': ('enrolled_students',)
        }),
    )

    def save_model(self, request, obj, form, change):
        form.save()  # 👈 This ensures enrollments are updated properly

admin.site.register(Class, ClassAdmin)
