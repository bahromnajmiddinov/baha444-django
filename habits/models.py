from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='🔥')
    color = models.CharField(max_length=7, default='#FF5722')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    target_days = models.IntegerField(default=7)  # For weekly habits
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def current_streak(self):
        completions = self.completions.filter(
            date__lte=timezone.now().date()
        ).order_by('-date')
        
        if not completions.exists():
            return 0
        
        streak = 0
        expected_date = timezone.now().date()
        
        for completion in completions:
            if completion.date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break
        
        return streak

    @property
    def total_completions(self):
        return self.completions.count()

    @property
    def completion_rate(self):
        days_since_creation = (timezone.now().date() - self.created_at.date()).days + 1
        if days_since_creation == 0:
            return 0
        return round((self.total_completions / days_since_creation) * 100, 1)


class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['habit', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
