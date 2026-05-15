from django.db import models
from users.models import PlayerProfile

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    @property
    def win_rate(self):
        total = self.wins + self.losses
        if total == 0:
            return 0
        return round((self.wins / total) * 100, 2)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('captain', 'Captain'),
        ('player', 'Player'),
        ('coach', 'Coach'),
        ('sub', 'Substitute'),
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'player')

    def __str__(self):
        return f"{self.player.user.username} - {self.team.name} ({self.role})"

class RecruitmentPost(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='recruitment_posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    roles_needed = models.CharField(max_length=255, help_text="e.g. IGL, AWPer, Entry Fragger")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team.name} - {self.title}"

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    post = models.ForeignKey(RecruitmentPost, on_delete=models.CASCADE, related_name='applications')
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField(blank=True, help_text="Why do you want to join?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'player') # Prevent duplicate applications

    def __str__(self):
        return f"{self.player.user.username} -> {self.post.team.name}"
