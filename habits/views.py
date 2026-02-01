from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Habit, HabitCompletion

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user, is_active=True)
    today = timezone.now().date()
    
    context = {
        'habits': habits,
        'today': today,
    }
    return render(request, 'habits/list.html', context)

@login_required
def habit_create(request):
    if request.method == 'POST':
        habit = Habit.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            icon=request.POST.get('icon', '🔥'),
            color=request.POST.get('color', '#FF5722'),
            frequency=request.POST.get('frequency', 'daily'),
        )
        return redirect('habit_list')
    return render(request, 'habits/create.html')

@login_required
def habit_toggle(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    
    completion, created = HabitCompletion.objects.get_or_create(
        habit=habit,
        date=today
    )
    
    if not created:
        completion.delete()
        completed = False
    else:
        completed = True
    
    return JsonResponse({'completed': completed, 'streak': habit.current_streak})
