from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class TaskTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_tags')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#6366f1')  # Hex color
    icon = models.CharField(max_length=50, default='tag', blank=True)  # Icon name from Heroicons
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'name')
    
    def __str__(self):
        return f"{self.name} ({self.user})"

class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_lists')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='list', blank=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position', '-created_at']
        unique_together = ('user', 'name')
    
    def __str__(self):
        return f"{self.name} ({self.user})"

class Task(models.Model):
    STATUS_CHOICES = [
        ('pitched', 'Pitched'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('paid', 'Paid'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pitched')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    estimated_duration = models.IntegerField(blank=True, null=True, help_text="Duration in minutes")
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    tags = models.ManyToManyField(TaskTag, blank=True, related_name='tasks')
    task_list = models.ForeignKey(TaskList, on_delete=models.SET_NULL, blank=True, null=True, related_name='tasks')
    attachments_count = models.IntegerField(default=0)
    google_task_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.due_date and self.status != 'completed':
            return timezone.now() > self.due_date
        return False


class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} - {self.task.title}"


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment on {self.task.title}"

class TaskActivity(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('completed', 'Completed'),
        ('reopened', 'Reopened'),
        ('archived', 'Archived'),
        ('restored', 'Restored'),
        ('pinned', 'Pinned'),
        ('unpinned', 'Unpinned'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(default=dict, blank=True)  # Stores what changed: {'field': 'old_value -> new_value'}
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} on {self.task.title} at {self.timestamp}"

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['position', '-created_at']
    
    def __str__(self):
        return f"{self.title} (parent: {self.task.title})"
