from django import forms
from .models import Tournament

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'format', 'start_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'game': forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'format': forms.Select(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white'}),
        }
