from django import forms
from .models import Team, RecruitmentPost, Application

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white', 'rows': 4}),
            'logo': forms.FileInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
        }

class RecruitmentPostForm(forms.ModelForm):
    class Meta:
        model = RecruitmentPost
        fields = ['title', 'description', 'roles_needed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'roles_needed': forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white', 'rows': 4}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white', 'rows': 3, 'placeholder': 'Tell them why you are a good fit...'}),
        }
