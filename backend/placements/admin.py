from django.contrib import admin
from .models import InternshipPlacement, WeeklyLog

@admin.register(InternshipPlacement)
class InternshipPlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'organizations', 'status', 'academic_supervisor')
    list_filter = ('status', 'organizations')
    search_fields = ('student__user__username', 'organizations__name')

@admin.register(WeeklyLog)
class WeeklyLogAdmin(admin.ModelAdmin):
    list_display = ('placement', 'week_number', 'submitted_at')
    list_filter = ('week_number',)