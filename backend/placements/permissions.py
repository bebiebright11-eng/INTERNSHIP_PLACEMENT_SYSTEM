from rest_framework import permissions

class IsAssignedSupervisor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj is the WeeklyLog
        placement = obj.placement
        return (
            request.user == placement.academic_supervisor or 
            request.user == placement.workplace_supervisor
        )