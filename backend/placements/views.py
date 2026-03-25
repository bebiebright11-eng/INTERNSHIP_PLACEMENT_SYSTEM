from rest_framework import generics, permissions
from .models import InternshipPlacement, WeeklyLog
from .serializers import InternshipPlacementSerializer, WeeklyLogSerializer
from .permissions import IsAssignedSupervisor # Import your new class
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser

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




class WeeklyLogReviewView(generics.UpdateAPIView):
    queryset = WeeklyLog.objects.all()
    serializer_class = WeeklyLogSerializer
    # Add the permission here!
    permission_classes = [IsAssignedSupervisor] 

    def perform_update(self, serializer):
        # You can also automate status changes here
        serializer.save(status='REVIEWED')        


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
    

class AssignedStudentsListView(generics.ListAPIView):
    serializer_class = InternshipPlacementSerializer # Assuming you have this
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User Story: "Only see students I am supervising"
        return InternshipPlacement.objects.filter(academic_supervisor=self.request.user)    
    


class FinalReportUploadView(generics.UpdateAPIView):
    queryset = InternshipPlacement.objects.all()
    serializer_class = InternshipPlacementSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # Required for file uploads

    def perform_update(self, serializer):
        # Security: Ensure only the student who owns the placement can upload
        if self.get_object().student.user != self.request.user:
            raise ValidationError("You can only upload reports for your own placement.")
        
        # Automatically set the submission timestamp
        serializer.save(report_submitted_at=timezone.now())    