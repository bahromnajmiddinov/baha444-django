from django.contrib import admin
from .models import Task, TaskAttachment, TaskComment, TaskTag, TaskList, TaskActivity, Subtask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'due_date', 'is_archived', 'is_pinned')
    list_filter = ('status', 'priority', 'is_archived', 'is_pinned', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)

@admin.register(TaskTag)
class TaskTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color', 'icon', 'created_at')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_archived', 'position', 'created_at')
    list_filter = ('user', 'is_archived')
    search_fields = ('name', 'description')

@admin.register(TaskActivity)
class TaskActivityAdmin(admin.ModelAdmin):
    list_display = ('task', 'action', 'user', 'timestamp')
    list_filter = ('action', 'timestamp')

@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'is_completed', 'position', 'created_at')
    list_filter = ('is_completed',)

admin.site.register(TaskAttachment)
admin.site.register(TaskComment)
