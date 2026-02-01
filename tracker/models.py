from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_entries')
    date = models.DateField(default=timezone.now)
    
    # Mood tracking
    mood = models.CharField(max_length=20, choices=[
        ('excellent', '😄 Excellent'),
        ('good', '🙂 Good'),
        ('okay', '😐 Okay'),
        ('bad', '🙁 Bad'),
        ('terrible', '😢 Terrible'),
    ], blank=True)
    
    # Energy level
    energy_level = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        null=True,
        blank=True
    )
    
    # Daily notes and reflections
    morning_notes = models.TextField(blank=True)
    evening_notes = models.TextField(blank=True)
    
    # What went well
    wins = models.TextField(blank=True)
    
    # Challenges
    challenges = models.TextField(blank=True)
    
    # Gratitude
    gratitude = models.TextField(blank=True)
    
    # Goals for tomorrow
    tomorrow_goals = models.TextField(blank=True)
    
    # Sleep tracking
    sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    sleep_quality = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        null=True,
        blank=True
    )
    
    # Water intake (glasses)
    water_intake = models.IntegerField(default=0)
    
    # Exercise
    exercise_minutes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        verbose_name_plural = 'Daily entries'

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class MoodLog(models.Model):
    """For tracking mood throughout the day"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    mood = models.CharField(max_length=20, choices=[
        ('excellent', '😄 Excellent'),
        ('good', '🙂 Good'),
        ('okay', '😐 Okay'),
        ('bad', '🙁 Bad'),
        ('terrible', '😢 Terrible'),
    ])
    notes = models.TextField(blank=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_mood_display()} at {self.logged_at}"


class CustomMetric(models.Model):
    """For tracking custom metrics like screen time, meditation, etc."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_metrics')
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)  # e.g., "minutes", "pages", "cups"
    icon = models.CharField(max_length=50, default='📊')
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"


class MetricEntry(models.Model):
    metric = models.ForeignKey(CustomMetric, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField(default=timezone.now)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['metric', 'date']
        ordering = ['-date']
        verbose_name_plural = 'Metric entries'

    def __str__(self):
        return f"{self.metric.name}: {self.value} on {self.date}"
