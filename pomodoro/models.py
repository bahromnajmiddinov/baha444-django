from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PomodoroSession(models.Model):
    SESSION_TYPES = [
        ('focus', 'Focus'),
        ('short_break', 'Short Break'),
        ('long_break', 'Long Break'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pomodoro_sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='focus')
    duration_minutes = models.IntegerField(default=25)
    completed_minutes = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='pomodoro_sessions')
    notes = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.get_session_type_display()} - {self.started_at.date()}"

    @property
    def completion_percentage(self):
        if self.duration_minutes == 0:
            return 0
        return min(100, round((self.completed_minutes / self.duration_minutes) * 100))


class PomodoroSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pomodoro_settings')
    focus_duration = models.IntegerField(default=25)
    short_break_duration = models.IntegerField(default=5)
    long_break_duration = models.IntegerField(default=15)
    sessions_until_long_break = models.IntegerField(default=4)
    auto_start_breaks = models.BooleanField(default=False)
    auto_start_pomodoros = models.BooleanField(default=False)
    sound_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Pomodoro Settings"
