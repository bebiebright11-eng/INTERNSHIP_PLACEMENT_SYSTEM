from rest_framework import permissions

class IsAssignedSupervisor(permissions.BasePermission):
    """
    Permission to only allow the assigned academic supervisor 
    to edit or add feedback to a weekly log.
    """
    def has_object_permission(self, request, view, obj):
        # 'obj' here is the WeeklyLog instance
        # We check if the logged-in user is the supervisor of that placement
        return obj.placement.academic_supervisor == request.user