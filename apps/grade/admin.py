from django.contrib import admin
from .models import GradingScheme
# Register your models here.

admin.site.register(GradingScheme)

# Ideally, grading schemes must be added immediately upon creation of Class instance.