from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tournament, TournamentRegistration
from .forms import TournamentForm
from teams.models import TeamMember

def tournament_list(request):
    tournaments = Tournament.objects.filter(is_active=True).order_by('start_date')
    return render(request, 'tournaments/tournament_list.html', {'tournaments': tournaments})

@login_required
def tournament_create(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            messages.success(request, f"Tournament '{tournament.name}' created successfully!")
            return redirect('tournaments:detail', pk=tournament.pk)
    else:
        form = TournamentForm()
    return render(request, 'tournaments/tournament_form.html', {'form': form})

def tournament_detail(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    return render(request, 'tournaments/tournament_detail.html', {'tournament': tournament})

@login_required
def tournament_register(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    memberships = TeamMember.objects.filter(player=request.user.player_profile, role__in=['captain', 'coach'])
    
    if not memberships.exists():
        messages.error(request, "You must be a team captain to register for tournaments.")
        return redirect('tournaments:detail', pk=pk)
        
    team = memberships.first().team
    
    if TournamentRegistration.objects.filter(tournament=tournament, team=team).exists():
        messages.warning(request, "Your team is already registered.")
        return redirect('tournaments:detail', pk=pk)

    if request.method == 'POST':
        TournamentRegistration.objects.create(tournament=tournament, team=team)
        messages.success(request, f"{team.name} successfully registered for {tournament.name}!")
        return redirect('tournaments:detail', pk=pk)
        
    return render(request, 'tournaments/tournament_register.html', {'tournament': tournament, 'team': team})
