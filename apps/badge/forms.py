# apps/badge/forms.py

from django import forms
from .models import BadgeShard

class BadgeShardForm(forms.ModelForm):
    class Meta:
        model = BadgeShard
        fields = ['type', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Reason for giving this badge...'}),
        }
