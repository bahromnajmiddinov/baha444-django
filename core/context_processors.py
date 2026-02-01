from tasks.models import TaskTag, TaskList

def user_task_context(request):
    """Add task lists and tags to the context for authenticated users."""
    if request.user.is_authenticated:
        return {
            'user_task_lists': TaskList.objects.filter(user=request.user, is_archived=False).order_by('position', '-created_at'),
            'user_tags': TaskTag.objects.filter(user=request.user).order_by('-created_at')[:10],  # Limit to 10 tags for performance
        }
    return {}
