from django.db import models
from django.conf import settings
from scrims.models import MatchDetails

class Replay(models.Model):
    match = models.ForeignKey(MatchDetails, on_delete=models.CASCADE, related_name='replays')
    video_file = models.FileField(upload_to='replays/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replay for {self.match}"

class HighlightMarker(models.Model):
    replay = models.ForeignKey(Replay, on_delete=models.CASCADE, related_name='markers')
    timestamp = models.CharField(max_length=10, help_text="e.g. 05:23")
    event_type = models.CharField(max_length=50) # e.g. Kill, Clutch
    
    def __str__(self):
        return f"{self.event_type} at {self.timestamp}"

class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=255) # e.g. 'joined team ESPNET'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action}"
