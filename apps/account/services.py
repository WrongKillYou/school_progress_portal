# apps/account/services/student_dashboard.py
from collections import defaultdict
from datetime import date
from django.utils import timezone

from announcement.models import Announcement
from attendance.models import Attendance
from badge.models import BadgeShard
from classroom.models import Class, Enrollment
from grade.models import FinalGrade, GradeItem


# ────────────────────────────────────────────────────────────
def get_enrolled_classes(student):
    """Return queryset of Class objects the student is enrolled in."""
    return (
        Class.objects.filter(enrollments__student=student)
        .select_related("teacher")
        .order_by("subject")
    )


# ────────────────────────────────────────────────────────────
def get_recent_announcements(classes, limit=10):
    """Latest announcements for the given classes."""
    return (
        Announcement.objects.filter(class_obj__in=classes)
        .select_related("teacher", "class_obj")
        .order_by("-date_posted")[:limit]
    )


# ────────────────────────────────────────────────────────────
# services/student_dashboard.py
# services.py

def build_grade_starplot_detail(student, classes):
    """
    Returns a nested dict:
    {
        "Math": {
            "1": { "final": 92, "components": [...] },
            "2": { "final": 89, "components": [...] },
            ...
        },
        ...
    }
    """
    detail = {}

    for cls in classes:
        subj = cls.subject
        for qtr in range(1, 5):
            fg = FinalGrade.objects.filter(
                student=student,
                class_obj=cls,
                quarter=qtr
            ).first()

            final = round(fg.final_grade) if fg and fg.final_grade is not None else 0

            components = list(
                GradeItem.objects.filter(
                    student=student,
                    class_obj=cls,
                    quarter=qtr
                ).values("component", "score", "highest_possible_score")
            )

            detail.setdefault(subj, {})[str(qtr)] = {
                "final": final,
                "components": components
            }

    return detail



import json
from grade.models import FinalGrade
def build_all_quarters_starplot(student):
    data = {}
    labels_set = set()

    enrolled_subjects = list(
        Enrollment.objects.filter(student=student)
        .select_related('class_obj')
        .values_list('class_obj__subject', flat=True)
    )

    for quarter in range(1, 5):
        grades = FinalGrade.objects.filter(student=student, quarter=quarter)
        posted_subjects = [fg.class_obj.subject for fg in grades]
        missing_subjects = [subj for subj in enrolled_subjects if subj not in posted_subjects]

        if grades.exists():
            labels = posted_subjects
            values = [fg.final_grade for fg in grades]
            labels_set.update(labels)
            data[quarter] = {
                "labels": labels,
                "values": values,
                "missing_subjects": missing_subjects
            }
        else:
            data[quarter] = {
                "labels": [],
                "values": [],
                "missing_subjects": missing_subjects
            }

    return json.dumps(data), list(labels_set)




# ────────────────────────────────────────────────────────────

# services/student_dashboard.py
from attendance.models import Attendance
from django.utils import timezone

def get_monthly_attendance(student, month=None, year=None):
    """
    Returns a list of dictionaries like:
    [
        {"date": "YYYY-MM-DD", "status": "present|absent|incomplete"},
        ...
    ]
    """
    today = timezone.localdate()
    month = month or today.month
    year  = year  or today.year

    records = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    ).only("date", "status", "time_in", "time_out")

    result = []
    for record in records:
        if record.status == 'absent':
            status = 'absent'
        elif record.status == 'excused':
            status = 'incomplete'  # 👈 use yellow for excused?
        elif record.time_in and record.time_out:
            status = 'present'
        elif record.time_in or record.time_out:
            status = 'incomplete'
        else:
            status = 'absent'  # fallback
        result.append({
            "date": record.date.isoformat(),
            "status": status,
        })
    return result



# ────────────────────────────────────────────────────────────

# apps/account/services.py
from badge.models import BadgeShard

def badge_breakdown(student):
    """
    Returns shard math ready for the template:
      • full_stars      – list range for each completed star
      • star_fragments  – 0-4 remaining lit arms
      • full_squares    – list range for each completed square
      • square_fragments– 0-3 remaining lit quadrants
    """
    merit_shards   = BadgeShard.objects.filter(student=student, type='merit').count()
    demerit_shards = BadgeShard.objects.filter(student=student, type='demerit').count()

    full_stars        = merit_shards // 5
    star_fragments    = merit_shards % 5

    full_squares      = demerit_shards // 4
    square_fragments  = demerit_shards % 4

    return {
        "full_stars":       list(range(full_stars)),   # e.g. [0,1] if two full stars
        "star_fragments":   star_fragments,            # 0-4
        "full_squares":     list(range(full_squares)), # list so we can {% for _ in ... %}
        "square_fragments": square_fragments,          # 0-3
    }


