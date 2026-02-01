from django.contrib import admin
from .models import PomodoroSession, PomodoroSettings

admin.site.register(PomodoroSession)
admin.site.register(PomodoroSettings)