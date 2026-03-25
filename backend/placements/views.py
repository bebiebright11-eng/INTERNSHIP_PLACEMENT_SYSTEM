from rest_framework import generics, permissions
from .models import InternshipPlacement, WeeklyLog
from .serializers import InternshipPlacementSerializer, WeeklyLogSerializer

class PlacementListCreateView(generics.ListCreateAPIView):
    serializer_class = InternshipPlacementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            # A student only sees their own placement record
            return InternshipPlacement.objects.filter(student__user=user)
        return InternshipPlacement.objects.all()

    def perform_create(self, serializer):
        # Automatically link the placement to the logged-in student's profile
        serializer.save(student=self.request.user.student_profile)

class WeeklyLogListCreateView(generics.ListCreateAPIView):
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show logs for the user's specific placement
        return WeeklyLog.objects.filter(placement__student__user=self.request.user)

        try:
            placement = InternshipPlacement.objects.get(id=placement_id)
        except InternshipPlacement.DoesNotExist:
            raise ValidationError({"error": "Placement record not found."})

        # 2. Check the Status Gate
        if placement.status != 'approved':
            raise ValidationError({
                "error": f"You cannot submit logs for a {placement.status} placement. "
                         "Please wait for supervisor approval."
            })

        # 3. If approved, save the log
        serializer.save()


class SupervisorLogReviewView(generics.UpdateAPIView, generics.ListAPIView):
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Ensure only Workplace Supervisors can see this
        if user.role == 'workplace_sup':
            # Filter logs: Only show logs for the organization this supervisor belongs to
            return WeeklyLog.objects.filter(
                placement__organizations=user.workplace_profile.organizations
            )
        return WeeklyLog.objects.none()