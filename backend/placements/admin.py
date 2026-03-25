from django.contrib import admin
from .models import InternshipPlacement, WeeklyLog

@admin.register(InternshipPlacement)
class InternshipPlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization', 'status', 'academic_supervisor')
    list_filter = ('status', 'organization', 'academic_supervisor')
    search_fields = ('student__username', 'organization__name')
    inlines = [WeeklyLogInline]

@admin.register(WeeklyLog)
class WeeklyLogAdmin(admin.ModelAdmin):
    list_display = ('placement', 'week_number', 'submitted_at')
    list_filter = ('week_number',)