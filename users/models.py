from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('player', 'Player'),
        ('team_admin', 'Team Admin'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')

    def __str__(self):
        return self.username

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player_profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    preferred_games = models.CharField(max_length=255, blank=True, help_text="Comma separated e.g. CS2, Valorant")
    rank = models.CharField(max_length=50, blank=True)
    kills = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)

    @property
    def kd_ratio(self):
        if self.deaths == 0:
            return self.kills
        return round(self.kills / self.deaths, 2)

    @property
    def win_rate(self):
        total = self.wins + self.losses
        if total == 0:
            return 0
        return round((self.wins / total) * 100, 2)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    badge_icon = models.ImageField(upload_to='badges/', blank=True, null=True)

    def __str__(self):
        return self.title

class PlayerAchievement(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.user.username} - {self.achievement.title}"

class Reputation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reputation')
    trust_score = models.IntegerField(default=100)
    total_ratings = models.IntegerField(default=0)
    positive_ratings = models.IntegerField(default=0)
    negative_ratings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Reputation: {self.trust_score}"
