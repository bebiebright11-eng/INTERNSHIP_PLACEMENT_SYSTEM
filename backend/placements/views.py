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