from django.db import models
from users.models import PlayerProfile

class PlayerStatSnapshot(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='stat_history')
    date = models.DateField(auto_now_add=True)
    win_rate = models.FloatField(default=0.0)
    kd_ratio = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('player', 'date')

    def __str__(self):
        return f"{self.player.user.username} Stats on {self.date}"
