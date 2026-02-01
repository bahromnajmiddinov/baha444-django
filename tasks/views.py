from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Task, TaskAttachment, TaskComment, TaskTag, TaskList, TaskActivity
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
            start_date=request.POST.get('start_date') or None,
            estimated_duration=request.POST.get('estimated_duration') or None,
            is_pinned=request.POST.get('is_pinned') in ['on', 'true', '1'],
        )

        task_list_id = request.POST.get('task_list')
        if task_list_id:
            task_list = TaskList.objects.filter(user=request.user, pk=task_list_id).first()
            if task_list:
                task.task_list = task_list
                task.save()

        tag_ids = request.POST.getlist('tags')
        if tag_ids:
            tags = TaskTag.objects.filter(user=request.user, id__in=tag_ids)
            task.tags.set(tags)

        TaskActivity.objects.create(
            task=task,
            action='created',
            user=request.user
        )

        if request.htmx:
            return render(request, 'tasks/partials/task_card.html', {'task': task})

        return redirect('task_list')

    task_lists = TaskList.objects.filter(user=request.user, is_archived=False)
    tags = TaskTag.objects.filter(user=request.user)
    context = {'task_lists': task_lists, 'tags': tags}

    return render(request, 'tasks/create.html', context)


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
        changes = {}

        new_title = request.POST.get('title', task.title)
        if new_title != task.title:
            changes['title'] = f"{task.title} → {new_title}"
            task.title = new_title

        new_status = request.POST.get('status', task.status)
        if new_status != task.status:
            changes['status'] = f"{task.status} → {new_status}"
            task.status = new_status

        new_description = request.POST.get('description', task.description)
        if new_description != task.description:
            changes['description'] = 'Updated description'
            task.description = new_description

        new_priority = request.POST.get('priority', task.priority)
        if new_priority != task.priority:
            changes['priority'] = f"{task.priority} → {new_priority}"
            task.priority = new_priority

        due_date_value = request.POST.get('due_date')
        if due_date_value:
            parsed_due_date = datetime.fromisoformat(due_date_value)
            if task.due_date != parsed_due_date:
                changes['due_date'] = f"{task.due_date} → {parsed_due_date}"
                task.due_date = parsed_due_date
        elif task.due_date:
            changes['due_date'] = f"{task.due_date} → None"
            task.due_date = None

        start_date_value = request.POST.get('start_date')
        if start_date_value:
            parsed_start_date = datetime.fromisoformat(start_date_value)
            if task.start_date != parsed_start_date:
                changes['start_date'] = f"{task.start_date} → {parsed_start_date}"
                task.start_date = parsed_start_date
        elif task.start_date:
            changes['start_date'] = f"{task.start_date} → None"
            task.start_date = None

        estimated_duration_value = request.POST.get('estimated_duration')
        if estimated_duration_value:
            parsed_duration = int(estimated_duration_value)
            if task.estimated_duration != parsed_duration:
                changes['estimated_duration'] = f"{task.estimated_duration} → {parsed_duration}"
                task.estimated_duration = parsed_duration
        elif task.estimated_duration is not None:
            changes['estimated_duration'] = f"{task.estimated_duration} → None"
            task.estimated_duration = None

        is_pinned = request.POST.get('is_pinned') in ['on', 'true', '1']
        if task.is_pinned != is_pinned:
            changes['is_pinned'] = f"{task.is_pinned} → {is_pinned}"
            task.is_pinned = is_pinned

        task_list_id = request.POST.get('task_list')
        if task_list_id:
            task_list = TaskList.objects.filter(user=request.user, pk=task_list_id).first()
            if task_list and task.task_list_id != task_list.id:
                changes['task_list'] = f"{task.task_list} → {task_list}"
                task.task_list = task_list
        elif task.task_list_id:
            changes['task_list'] = f"{task.task_list} → None"
            task.task_list = None

        if task.status == 'completed' and not task.completed_date:
            task.completed_date = timezone.now()
            changes['completed'] = 'Task marked complete'
        elif task.status != 'completed' and task.completed_date:
            task.completed_date = None
            changes['reopened'] = 'Task reopened'

        task.save()

        tag_ids = request.POST.getlist('tags')
        if tag_ids is not None:
            tags = TaskTag.objects.filter(user=request.user, id__in=tag_ids)
            task.tags.set(tags)

        if changes:
            TaskActivity.objects.create(
                task=task,
                action='updated',
                user=request.user,
                changes=changes
            )

        if request.htmx:
            return render(request, 'tasks/partials/task_card.html', {'task': task})

        return redirect('task_detail', pk=task.pk)

    task_lists = TaskList.objects.filter(user=request.user, is_archived=False)
    tags = TaskTag.objects.filter(user=request.user)
    context = {'task': task, 'task_lists': task_lists, 'tags': tags}

    return render(request, 'tasks/update.html', context)


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

    new_status = data.get('status', task.status)
    new_position = data.get('position', task.position)
    changes = {}

    if new_status != task.status:
        changes['status'] = f"{task.status} → {new_status}"
        task.status = new_status

    if new_position != task.position:
        task.position = new_position

    if task.status == 'completed' and not task.completed_date:
        task.completed_date = timezone.now()
        changes['completed'] = 'Task marked complete'
    elif task.status != 'completed' and task.completed_date:
        task.completed_date = None
        changes['reopened'] = 'Task reopened'

    task.save()

    if changes:
        TaskActivity.objects.create(
            task=task,
            action='updated',
            user=request.user,
            changes=changes
        )

    return JsonResponse({'success': True})


@login_required
def calendar_view(request):
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))

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

    tasks_by_day = {}
    for task in tasks:
        day = task.due_date.day
        if day not in tasks_by_day:
            tasks_by_day[day] = []
        tasks_by_day[day].append(task)

    import calendar
    cal = calendar.monthcalendar(year, month)
    
    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'tasks_by_day': tasks_by_day,
        'calendar': cal,
        'prev_month': month - 1 if month > 1 else 12,
        'prev_year': year if month > 1 else year - 1,
        'next_month': month + 1 if month < 12 else 1,
        'next_year': year if month < 12 else year + 1,
    }

    return render(request, 'tasks/calendar.html', context)


@login_required
def task_toggle_pin(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_pinned = not task.is_pinned
    task.save()

    TaskActivity.objects.create(
        task=task,
        action='pinned' if task.is_pinned else 'unpinned',
        user=request.user
    )

    if request.htmx:
        return render(request, 'tasks/partials/task_card.html', {'task': task})

    return JsonResponse({'success': True, 'is_pinned': task.is_pinned})


@login_required
def task_archive(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_archived = True
    task.archived_at = timezone.now()
    task.save()

    TaskActivity.objects.create(
        task=task,
        action='archived',
        user=request.user
    )

    if request.htmx:
        return JsonResponse({'success': True})

    return redirect('task_list')


@login_required
def task_activity_log(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    activities = task.activities.all()[:50]

    context = {'task': task, 'activities': activities}
    return render(request, 'tasks/activity_log.html', context)


@login_required
def tag_list(request):
    tags = TaskTag.objects.filter(user=request.user).annotate(
        task_count=Count('tasks')
    ).order_by('-created_at')

    context = {'tags': tags}
    return render(request, 'tasks/tag_list.html', context)


@login_required
def tag_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color', '#6366f1')
        icon = request.POST.get('icon', 'tag')

        tag, created = TaskTag.objects.get_or_create(
            user=request.user,
            name=name,
            defaults={'color': color, 'icon': icon}
        )

        if not created:
            tag.color = color
            tag.icon = icon
            tag.save()

        if request.htmx:
            tags = TaskTag.objects.filter(user=request.user).annotate(task_count=Count('tasks'))
            return render(request, 'tasks/partials/tag_list.html', {'tags': tags})

        return redirect('tag_list')

    return render(request, 'tasks/tag_create.html')


@login_required
def tag_detail(request, pk):
    tag = get_object_or_404(TaskTag, pk=pk, user=request.user)
    tasks = tag.tasks.filter(user=request.user).order_by('-created_at')

    context = {'tag': tag, 'tasks': tasks}
    return render(request, 'tasks/tag_detail.html', context)


@login_required
def tag_update(request, pk):
    tag = get_object_or_404(TaskTag, pk=pk, user=request.user)

    if request.method == 'POST':
        tag.name = request.POST.get('name', tag.name)
        tag.color = request.POST.get('color', tag.color)
        tag.icon = request.POST.get('icon', tag.icon)
        tag.save()

        if request.htmx:
            return render(request, 'tasks/partials/tag_item.html', {'tag': tag})

        return redirect('tag_detail', pk=tag.pk)

    return render(request, 'tasks/tag_update.html', {'tag': tag})


@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(TaskTag, pk=pk, user=request.user)

    if request.method == 'POST':
        tag.delete()

        if request.htmx:
            return JsonResponse({'success': True})

        return redirect('tag_list')

    return render(request, 'tasks/tag_confirm_delete.html', {'tag': tag})


@login_required
def tasklist_list(request):
    lists = TaskList.objects.filter(user=request.user, is_archived=False).order_by('position')
    archived_lists = TaskList.objects.filter(user=request.user, is_archived=True)

    context = {'lists': lists, 'archived_lists': archived_lists}
    return render(request, 'tasks/tasklist_list.html', context)


@login_required
def tasklist_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        icon = request.POST.get('icon', 'list')

        task_list = TaskList.objects.create(
            user=request.user,
            name=name,
            description=description,
            icon=icon
        )

        if request.htmx:
            return render(request, 'tasks/partials/tasklist_item.html', {'list': task_list})

        return redirect('tasklist_list')

    return render(request, 'tasks/tasklist_create.html')


@login_required
def tasklist_detail(request, pk):
    task_list = get_object_or_404(TaskList, pk=pk, user=request.user)
    tasks = task_list.tasks.all().order_by('-created_at')

    context = {'list': task_list, 'tasks': tasks}
    return render(request, 'tasks/tasklist_detail.html', context)


@login_required
def tasklist_update(request, pk):
    task_list = get_object_or_404(TaskList, pk=pk, user=request.user)

    if request.method == 'POST':
        task_list.name = request.POST.get('name', task_list.name)
        task_list.description = request.POST.get('description', task_list.description)
        task_list.icon = request.POST.get('icon', task_list.icon)
        task_list.save()

        if request.htmx:
            return render(request, 'tasks/partials/tasklist_item.html', {'list': task_list})

        return redirect('tasklist_detail', pk=task_list.pk)

    return render(request, 'tasks/tasklist_update.html', {'list': task_list})


@login_required
def tasklist_archive(request, pk):
    task_list = get_object_or_404(TaskList, pk=pk, user=request.user)

    if request.method == 'POST':
        task_list.is_archived = True
        task_list.archived_at = timezone.now()
        task_list.save()

        if request.htmx:
            return JsonResponse({'success': True})

        return redirect('tasklist_list')

    return render(request, 'tasks/tasklist_confirm_archive.html', {'list': task_list})


@login_required
def dashboard_enhanced(request):
    user_tasks = Task.objects.filter(user=request.user, is_archived=False)
    today = timezone.now().date()

    tasks_today = user_tasks.filter(due_date__date=today)

    overdue_tasks = user_tasks.filter(
        due_date__lt=timezone.now(),
        status__in=['pitched', 'in_progress']
    )

    upcoming_tasks = user_tasks.filter(
        due_date__date__gte=today,
        due_date__date__lte=today + timedelta(days=7),
        status__in=['pitched', 'in_progress']
    ).order_by('due_date')

    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='completed').count()
    pending_tasks = user_tasks.filter(status__in=['pitched', 'in_progress']).count()
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    high_priority_tasks = user_tasks.filter(priority='high').count()

    context = {
        'tasks_today': tasks_today,
        'overdue_tasks': overdue_tasks,
        'upcoming_tasks': upcoming_tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': round(completion_percentage, 1),
        'high_priority_tasks': high_priority_tasks,
        'overdue_count': overdue_tasks.count(),
    }

    return render(request, 'tasks/dashboard.html', context)
