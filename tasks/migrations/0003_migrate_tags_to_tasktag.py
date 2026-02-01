from django.db import migrations

def migrate_tags(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    TaskTag = apps.get_model('tasks', 'TaskTag')
    
    for task in Task.objects.all():
        if task.tags_old:
            tag_names = [t.strip() for t in task.tags_old.split(',') if t.strip()]
            for name in tag_names:
                tag, created = TaskTag.objects.get_or_create(
                    user=task.user,
                    name=name
                )
                task.tags.add(tag)

class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0002_task_archived_at_task_estimated_duration_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_tags),
    ]
