from django.db import models

class Scrim(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    game = models.CharField(max_length=100)
    requester = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='requested_scrims')
    opponent = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_scrims')
    date_time = models.DateTimeField()
    format = models.CharField(max_length=50, help_text="e.g. BO1, BO3")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.name} Scrim ({self.game})"

class MatchDetails(models.Model):
    scrim = models.OneToOneField(Scrim, on_delete=models.CASCADE, related_name='match_details')
    requester_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    mvp = models.ForeignKey('users.PlayerProfile', on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(blank=True)

    def __str__(self):
        return f"Result: {self.scrim.requester.name} {self.requester_score} - {self.opponent_score} {self.scrim.opponent.name if self.scrim.opponent else 'TBA'}"
