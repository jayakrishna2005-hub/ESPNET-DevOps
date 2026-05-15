from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PlayerProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = ['bio', 'avatar', 'preferred_games', 'rank']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded p-2 text-white', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded p-2 text-white'}),
            'preferred_games': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded p-2 text-white'}),
            'rank': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded p-2 text-white'}),
        }
