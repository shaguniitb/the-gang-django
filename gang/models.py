from django.db import models
from django.contrib.auth.models import User

class GameRoom(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Players'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]

    title = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_games')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def player_count(self):
        return self.players.count()

    def can_start(self):
        return 4 <= self.player_count() <= 10 and self.status == 'waiting'

class RoomPlayer(models.Model):
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE, related_name='players')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Custom name shown in lobbies and leaderboards (max 30 chars)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def get_display_name(self):
        """Returns the custom display name if it exists, otherwise defaults to the username."""
        return self.display_name if self.display_name else self.user.username
