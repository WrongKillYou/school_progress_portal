from django import forms
from .models import Student, User
from django.contrib.auth.forms import PasswordChangeForm

class StudentLoginForm(forms.Form):
    lrn = forms.CharField(max_length=50)

    def clean_lrn(self):
        lrn = self.cleaned_data.get('lrn')
        if not Student.objects.filter(lrn=lrn).exists():
            raise forms.ValidationError("Invalid LRN")
        return lrn
    

class TeacherLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Invalid username")
        return username


class TeacherPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter old password'})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )
