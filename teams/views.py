from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, TeamMember, RecruitmentPost, Application
from .forms import TeamForm, RecruitmentPostForm, ApplicationForm

def team_list(request):
    teams = Team.objects.all().order_by('-wins')
    return render(request, 'teams/team_list.html', {'teams': teams})

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'teams/team_detail.html', {'team': team})

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save()
            TeamMember.objects.create(team=team, player=request.user.player_profile, role='captain')
            messages.success(request, f"Team {team.name} created successfully!")
            return redirect('teams:detail', pk=team.pk)
    else:
        form = TeamForm()
    return render(request, 'teams/team_form.html', {'form': form})

@login_required
def team_dashboard(request, pk):
    team = get_object_or_404(Team, pk=pk)
    membership = TeamMember.objects.filter(team=team, player=request.user.player_profile).first()
    if not membership or membership.role not in ['captain', 'coach']:
        messages.error(request, "You do not have permission to manage this team.")
        return redirect('teams:detail', pk=pk)
    return render(request, 'teams/dashboard.html', {'team': team})

@login_required
def create_recruitment_post(request, pk):
    team = get_object_or_404(Team, pk=pk)
    membership = TeamMember.objects.filter(team=team, player=request.user.player_profile).first()
    if not membership or membership.role not in ['captain', 'coach']:
        return redirect('teams:detail', pk=pk)
        
    if request.method == 'POST':
        form = RecruitmentPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.team = team
            post.save()
            messages.success(request, "Recruitment post created!")
            return redirect('teams:dashboard', pk=team.pk)
    else:
        form = RecruitmentPostForm()
    return render(request, 'teams/recruitment_form.html', {'form': form, 'team': team})

@login_required
def apply_for_team(request, post_id):
    post = get_object_or_404(RecruitmentPost, pk=post_id)
    if Application.objects.filter(post=post, player=request.user.player_profile).exists():
        messages.warning(request, "You have already applied for this opening.")
        return redirect('teams:detail', pk=post.team.pk)
        
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.post = post
            app.player = request.user.player_profile
            app.save()
            messages.success(request, f"Application sent to {post.team.name}!")
            return redirect('teams:detail', pk=post.team.pk)
    else:
        form = ApplicationForm()
    return render(request, 'teams/apply_form.html', {'form': form, 'post': post})

@login_required
def review_application(request, app_id, action):
    app = get_object_or_404(Application, pk=app_id)
    # Check if reviewing user is captain/coach of the team
    team = app.post.team
    membership = TeamMember.objects.filter(team=team, player=request.user.player_profile).first()
    if not membership or membership.role not in ['captain', 'coach']:
        messages.error(request, "Permission denied.")
        return redirect('home')

    if action == 'accept':
        app.status = 'accepted'
        app.save()
        # Add to team
        TeamMember.objects.get_or_create(team=team, player=app.player, defaults={'role': 'player'})
        messages.success(request, f"Accepted {app.player.user.username} to the team!")
    elif action == 'reject':
        app.status = 'rejected'
        app.save()
        messages.success(request, "Application rejected.")
    return redirect('teams:dashboard', pk=team.pk)
