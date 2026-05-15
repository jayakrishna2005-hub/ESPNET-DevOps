from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, PlayerProfileForm
from .models import PlayerProfile

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile_edit(request):
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PlayerProfileForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')
