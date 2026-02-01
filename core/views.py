from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from tasks.models import Task
from habits.models import Habit, HabitCompletion
from pomodoro.models import PomodoroSession
from finance.models import Transaction, Budget, Account
from notes.models import Note, Reminder
from tracker.models import DailyEntry, MoodLog

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    # Tasks statistics
    tasks_total = Task.objects.filter(user=request.user).count()
    tasks_completed = Task.objects.filter(user=request.user, status='completed').count()
    tasks_in_progress = Task.objects.filter(user=request.user, status='in_progress').count()
    tasks_today = Task.objects.filter(
        user=request.user,
        due_date__date=today
    ).exclude(status='completed')
    
    # Habits
    habits = Habit.objects.filter(user=request.user, is_active=True)
    today_completions = HabitCompletion.objects.filter(
        habit__user=request.user,
        date=today
    ).values_list('habit_id', flat=True)
    
    # Pomodoro
    pomodoro_today = PomodoroSession.objects.filter(
        user=request.user,
        started_at__date=today,
        session_type='focus',
        is_completed=True
    ).count()
    
    # Finance
    this_month = datetime.now().replace(day=1).date()
    income = Transaction.objects.filter(
        user=request.user,
        category__category_type='income',
        date__gte=this_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses = Transaction.objects.filter(
        user=request.user,
        category__category_type='expense',
        date__gte=this_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent notes
    recent_notes = Note.objects.filter(
        user=request.user,
        is_archived=False
    )[:5]
    
    # Upcoming reminders
    upcoming_reminders = Reminder.objects.filter(
        user=request.user,
        is_completed=False,
        remind_at__gte=timezone.now()
    )[:5]
    
    # Daily entry
    daily_entry, created = DailyEntry.objects.get_or_create(
        user=request.user,
        date=today
    )
    
    context = {
        'tasks_total': tasks_total,
        'tasks_completed': tasks_completed,
        'tasks_in_progress': tasks_in_progress,
        'tasks_today': tasks_today,
        'habits': habits,
        'today_completions': list(today_completions),
        'pomodoro_today': pomodoro_today,
        'income': income,
        'expenses': expenses,
        'balance': income - expenses,
        'recent_notes': recent_notes,
        'upcoming_reminders': upcoming_reminders,
        'daily_entry': daily_entry,
        'today': today,
    }
    
    return render(request, 'dashboard.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
