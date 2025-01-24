# jobs/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, JobPost, JobApplication

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('user_type', 'phone_number', 'location', 'about')

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        exclude = ['employer', 'created_at', 'is_active']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter']

from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'location', 'about', 'profile_picture']        