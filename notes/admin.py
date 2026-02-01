from django.contrib import admin
from .models import Folder, Tag, Note, Idea, Reminder

admin.site.register(Folder)
admin.site.register(Tag)
admin.site.register(Note)
admin.site.register(Idea)
admin.site.register(Reminder)