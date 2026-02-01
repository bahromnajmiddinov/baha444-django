from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Task, TaskAttachment, TaskComment
import json
from datetime import datetime, timedelta

@login_required
def task_list(request):
    view_type = request.GET.get('view', 'list')
    filter_status = request.GET.get('status', 'all')
    
    tasks = Task.objects.filter(user=request.user)
    
    if filter_status != 'all':
        tasks = tasks.filter(status=filter_status)
    
    context = {
        'tasks': tasks,
        'view_type': view_type,
        'filter_status': filter_status,
    }
    
    if view_type == 'kanban':
        return render(request, 'tasks/kanban.html', context)
    elif view_type == 'calendar':
        return render(request, 'tasks/calendar.html', context)
    else:
        return render(request, 'tasks/list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        task = Task.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            status=request.POST.get('status', 'pitched'),
            priority=request.POST.get('priority', 'medium'),
            due_date=request.POST.get('due_date') or None,
        )
        
        if request.htmx:
            return render(request, 'tasks/partials/task_card.html', {'task': task})
        
        return redirect('task_list')
    
    return render(request, 'tasks/create.html')


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    comments = task.comments.all()
    attachments = task.attachments.all()
    
    context = {
        'task': task,
        'comments': comments,
        'attachments': attachments,
    }
    
    return render(request, 'tasks/detail.html', context)


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.status = request.POST.get('status', task.status)
        task.priority = request.POST.get('priority', task.priority)
        
        due_date_str = request.POST.get('due_date')
        if due_date_str:
            task.due_date = datetime.fromisoformat(due_date_str)
        
        if task.status == 'completed' and not task.completed_date:
            task.completed_date = timezone.now()
        
        task.save()
        
        if request.htmx:
            return render(request, 'tasks/partials/task_card.html', {'task': task})
        
        return redirect('task_detail', pk=task.pk)
    
    return render(request, 'tasks/update.html', {'task': task})


@login_required
@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    
    if request.htmx:
        return JsonResponse({'success': True})
    
    return redirect('task_list')


@login_required
@require_POST
def task_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    data = json.loads(request.body)
    
    task.status = data.get('status', task.status)
    task.position = data.get('position', task.position)
    
    if task.status == 'completed' and not task.completed_date:
        task.completed_date = timezone.now()
    
    task.save()
    
    return JsonResponse({'success': True})


@login_required
def calendar_view(request):
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Get all tasks for the month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    tasks = Task.objects.filter(
        user=request.user,
        due_date__gte=start_date,
        due_date__lt=end_date
    )
    
    # Group tasks by day
    tasks_by_day = {}
    for task in tasks:
        day = task.due_date.day
        if day not in tasks_by_day:
            tasks_by_day[day] = []
        tasks_by_day[day].append(task)
    
    context = {
        'year': year,
        'month': month,
        'tasks_by_day': tasks_by_day,
    }
    
    return render(request, 'tasks/calendar.html', context)
