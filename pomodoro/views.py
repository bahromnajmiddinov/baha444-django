from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import PomodoroSession, PomodoroSettings

@login_required
def pomodoro_view(request):
    settings, created = PomodoroSettings.objects.get_or_create(user=request.user)
    recent_sessions = PomodoroSession.objects.filter(user=request.user)[:10]
    
    context = {
        'settings': settings,
        'recent_sessions': recent_sessions,
    }
    return render(request, 'pomodoro/timer.html', context)

@login_required
def start_session(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        session = PomodoroSession.objects.create(
            user=request.user,
            session_type=data.get('session_type', 'focus'),
            duration_minutes=data.get('duration', 25),
        )
        
        return JsonResponse({'session_id': session.id})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def complete_session(request, pk):
    session = PomodoroSession.objects.get(pk=pk, user=request.user)
    session.is_completed = True
    session.completed_at = timezone.now()
    session.completed_minutes = session.duration_minutes
    session.save()
    
    return JsonResponse({'success': True})
