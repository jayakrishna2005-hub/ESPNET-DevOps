from django import forms
from .models import Scrim, MatchDetails

class ScrimForm(forms.ModelForm):
    class Meta:
        model = Scrim
        fields = ['game', 'date_time', 'format']
        widgets = {
            'game': forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white', 'placeholder': 'e.g. Valorant, CS2'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'format': forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white', 'placeholder': 'e.g. BO1, BO3, Scrim'}),
        }

class MatchDetailsForm(forms.ModelForm):
    class Meta:
        model = MatchDetails
        fields = ['requester_score', 'opponent_score', 'mvp', 'summary']
        widgets = {
            'requester_score': forms.NumberInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'opponent_score': forms.NumberInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'mvp': forms.Select(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'summary': forms.Textarea(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white', 'rows': 4}),
        }
