from django.contrib import admin
from .models import InternshipPlacement, WeeklyLog

class WeeklyLogInline(admin.TabularInline):
    model = WeeklyLog
    extra = 1 # Shows one empty row to add a log quickly

@admin.register(InternshipPlacement)
class InternshipPlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'organizations', 'status', 'academic_supervisor')
    list_filter = ('status', 'organizations', 'academic_supervisor')
    search_fields = ('student__username', 'organization__name')
    inlines = [WeeklyLogInline]

@admin.register(WeeklyLog)
class WeeklyLogAdmin(admin.ModelAdmin):
    list_display = ('placement', 'week_number', 'submitted_at')
    list_filter = ('week_number',)
