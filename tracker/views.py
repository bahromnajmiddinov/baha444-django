from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DailyEntry, MoodLog, CustomMetric

@login_required
def tracker_dashboard(request):
    today = timezone.now().date()
    daily_entry, created = DailyEntry.objects.get_or_create(
        user=request.user,
        date=today
    )
    
    recent_entries = DailyEntry.objects.filter(user=request.user)[:7]
    mood_logs = MoodLog.objects.filter(user=request.user)[:10]
    custom_metrics = CustomMetric.objects.filter(user=request.user, is_active=True)
    
    context = {
        'daily_entry': daily_entry,
        'recent_entries': recent_entries,
        'mood_logs': mood_logs,
        'custom_metrics': custom_metrics,
        'today': today,
    }
    
    return render(request, 'tracker/dashboard.html', context)
