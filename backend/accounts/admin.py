from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, AcademicSupervisorProfile, Organization

class CustomUserAdmin(UserAdmin):
    # Add 'role' to the fieldsets so it appears when editing a user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    # Add 'role' to the creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(AcademicSupervisorProfile)
admin.site.register(Organization)