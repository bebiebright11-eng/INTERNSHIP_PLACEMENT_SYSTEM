from django.contrib import admin
from .models import InternshipPlacement, WeeklyLog

class WeeklyLogInline(admin.TabularInline):
    model = WeeklyLog
    extra = 0
    fields = ('week_number', 'tasks_performed', 'supervisor_feedback', 'status')
    readonly_fields = ('submitted_at',)

@admin.register(InternshipPlacement)
class InternshipPlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'organizations', 'status', 'academic_supervisor','is_eligible')

    actions = ['verify_and_approve_placements']

    # Custom function to show a Green/Red checkmark for eligibility
    def is_eligible(self, obj):
        # Logic: A student is eligible if they have a Reg No and a Course
        return bool(obj.student.registration_number and obj.student.course)
    is_eligible.boolean = True # This makes it a nice icon in the UI

    # The "Bulk Action" for the Admin
    @admin.action(description="Verify and Approve selected placements")
    def verify_and_approve_placements(self, request, queryset):
        for placement in queryset:
            if self.is_eligible(placement):
                placement.status = 'APPROVED'
                placement.save()
            else:
                self.message_user(
                    request, 
                    f"Failed: {placement.student} is missing Reg No or Course data.", 
                    level='error'
                )

    search_fields = (
        'student__user__username', 
        'student__user__first_name', 
        'student__user__last_name', 
        'organization__name'
    )
    
    # 3. SIDEBAR FILTERS
    list_filter = ('status', 'organizations', 'academic_supervisor')
    
    # 4. CLICKABLE FIELDS
    list_display_links = ('student',)
    
    inlines = [WeeklyLogInline]

@admin.register(WeeklyLog)
class WeeklyLogAdmin(admin.ModelAdmin):
    list_display = ('placement', 'week_number', 'submitted_at','status')
    list_filter = ('status','submitted_at')    
# Inside InternshipPlacementAdmin
    search_fields = ('placement__student__user__username', 'tasks_performed')