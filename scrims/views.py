from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Scrim, MatchDetails
from .forms import ScrimForm, MatchDetailsForm
from teams.models import Team, TeamMember

def scrim_list(request):
    open_scrims = Scrim.objects.filter(status='open').order_by('date_time')
    completed_scrims = Scrim.objects.filter(status='completed').order_by('-date_time')[:10]
    return render(request, 'scrims/scrim_list.html', {'open_scrims': open_scrims, 'completed_scrims': completed_scrims})

@login_required
def scrim_create(request):
    # User must be captain of a team to create
    memberships = TeamMember.objects.filter(player=request.user.player_profile, role__in=['captain', 'coach'])
    if not memberships.exists():
        messages.error(request, "You must be a team captain or coach to request a scrim.")
        return redirect('scrims:list')
        
    team = memberships.first().team

    if request.method == 'POST':
        form = ScrimForm(request.POST)
        if form.is_valid():
            scrim = form.save(commit=False)
            scrim.requester = team
            scrim.save()
            messages.success(request, "Scrim request posted!")
            return redirect('scrims:list')
    else:
        form = ScrimForm()
    return render(request, 'scrims/scrim_form.html', {'form': form, 'team': team})

@login_required
def scrim_accept(request, pk):
    scrim = get_object_or_404(Scrim, pk=pk)
    memberships = TeamMember.objects.filter(player=request.user.player_profile, role__in=['captain', 'coach'])
    
    if not memberships.exists():
        messages.error(request, "You must be a team captain to accept a scrim.")
        return redirect('scrims:list')
        
    team = memberships.first().team
    
    if team == scrim.requester:
        messages.error(request, "You cannot accept your own scrim.")
        return redirect('scrims:list')

    if request.method == 'POST':
        scrim.opponent = team
        scrim.status = 'scheduled'
        scrim.save()
        messages.success(request, f"Scrim scheduled against {scrim.requester.name}!")
        return redirect('scrims:list')
        
    return render(request, 'scrims/scrim_accept.html', {'scrim': scrim, 'team': team})

@login_required
def scrim_report(request, pk):
    scrim = get_object_or_404(Scrim, pk=pk)
    if scrim.status != 'scheduled':
        messages.error(request, "Only scheduled scrims can be reported.")
        return redirect('scrims:list')
        
    if request.method == 'POST':
        form = MatchDetailsForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.scrim = scrim
            match.save()
            scrim.status = 'completed'
            
            # Simple win logic
            if match.requester_score > match.opponent_score:
                scrim.requester.wins += 1
                scrim.opponent.losses += 1
            else:
                scrim.opponent.wins += 1
                scrim.requester.losses += 1
                
            scrim.requester.save()
            scrim.opponent.save()
            scrim.save()
            
            messages.success(request, "Match results recorded! Stats updated.")
            return redirect('scrims:list')
    else:
        # Limit MVP choices to players in these two teams
        form = MatchDetailsForm()
        # form.fields['mvp'].queryset = PlayerProfile.objects.filter(team_memberships__team__in=[scrim.requester, scrim.opponent])
        
    return render(request, 'scrims/scrim_report.html', {'form': form, 'scrim': scrim})
