from django.db import models
from account.models import Student
from classroom.models import Class

# For weight configuration per class (since each subject may have its own scheme)
class GradingScheme(models.Model):
    class_obj = models.OneToOneField(Class, on_delete=models.CASCADE, related_name='grading_scheme')
    written_work_weight = models.FloatField(default=0.4)
    performance_task_weight = models.FloatField(default=0.4)
    quarterly_assessment_weight = models.FloatField(default=0.2)

    def __str__(self):
        return f"Grading Scheme for {self.class_obj}"


# Each score entry by component
class GradeItem(models.Model):
    COMPONENT_CHOICES = [
        ('WW', 'Written Work'),
        ('PT', 'Performance Task'),
        ('QA', 'Quarterly Assessment'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    component = models.CharField(max_length=2, choices=COMPONENT_CHOICES)
    score = models.FloatField()
    highest_possible_score = models.FloatField()

    def percentage_score(self):
        if self.highest_possible_score == 0:
            return 0.0
        return (self.score / self.highest_possible_score) * 100

    def __str__(self):
        return f"{self.student} - {self.component} - {self.score}/{self.highest_possible_score}"


# Summary model to compute total grade
class FinalGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    final_grade = models.FloatField(blank=True, null=True)  # Can be computed and saved

    class Meta:
        unique_together = ('student', 'class_obj')

    def compute_final_grade(self):
        items = GradeItem.objects.filter(student=self.student, class_obj=self.class_obj)
        scheme = self.class_obj.grading_scheme

        total_scores = {'WW': 0, 'PT': 0, 'QA': 0}
        total_highest = {'WW': 0, 'PT': 0, 'QA': 0}

        for item in items:
            total_scores[item.component] += item.score
            total_highest[item.component] += item.highest_possible_score

        def weighted(component, weight):
            if total_highest[component] == 0:
                return 0
            percent = (total_scores[component] / total_highest[component]) * 100
            return percent * weight

        final = sum([
            weighted('WW', scheme.written_work_weight),
            weighted('PT', scheme.performance_task_weight),
            weighted('QA', scheme.quarterly_assessment_weight),
        ])

        self.final_grade = round(final, 2)
        self.save()
        return self.final_grade

    def __str__(self):
        return f"{self.student} - {self.class_obj} = {self.final_grade if self.final_grade else 'Not yet computed'}"

