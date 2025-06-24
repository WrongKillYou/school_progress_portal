from django import forms
from .models import BadgeShard

class BadgeShardForm(forms.ModelForm):
    class Meta:
        model = BadgeShard
        fields = ['type', 'reason']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Reason for giving this badge...'
            }),
        }
