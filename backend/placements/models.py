from django.db import models
from django.conf import settings
from organizations.models import Organization
# Import the profile to ensure we link correctly
from accounts.models import StudentProfile 

class InternshipPlacement(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    # Change 1: Link to StudentProfile instead of just User
    student = models.OneToOneField(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='placement'
    )
    
    # Change 2: Matches your 'organizations' app name
    organizations = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name='placements'
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    workplace_supervisor = models.CharField(max_length=255, blank=True)
    
    # Change 3: Points to the User model but filters for the correct role
    academic_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='supervised_placements',
        limit_choices_to={'role': 'academic_sup'} 
    )

    final_score = models.IntegerField(null=True, blank=True)
    final_evaluation_comments = models.TextField(blank=True)

    def __str__(self):
        # FIX: Changed 'organization' to 'organizations' to match the field name
        return f"{self.student.user.username} at {self.organizations.name}"

class WeeklyLog(models.Model):
    placement = models.ForeignKey(
        InternshipPlacement, 
        on_delete=models.CASCADE, 
        related_name='logs'
    )

    
    week_number = models.PositiveIntegerField()
    tasks_performed = models.TextField()
    
    # --- ADD THIS STATUS FIELD ---
    LOG_STATUS = [
        ('SUBMITTED', 'Submitted'),
        ('REVIEWED', 'Reviewed'),
    ]
    status = models.CharField(max_length=20, choices=LOG_STATUS, default='SUBMITTED')
    # -----------------------------

    challenges = models.TextField(blank=True)
    attendance_days = models.PositiveIntegerField(default=5)
    supervisor_feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    