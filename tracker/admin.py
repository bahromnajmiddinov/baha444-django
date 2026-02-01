from django.contrib import admin
from .models import DailyEntry, MoodLog, CustomMetric, MetricEntry

admin.site.register(DailyEntry)
admin.site.register(MoodLog)
admin.site.register(CustomMetric)
admin.site.register(MetricEntry)