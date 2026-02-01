from django import template

register = template.Library()

@register.filter
def filter_status(tasks, status):
    return [task for task in tasks if task.status == status]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
