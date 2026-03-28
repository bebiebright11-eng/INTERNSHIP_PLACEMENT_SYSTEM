from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from organizations.models import Organization
# Import the profile to ensure we link correctly
from accounts.models import StudentProfile 

class InternshipPlacement(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    student = models.OneToOneField(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='placement'
    )
    
    # You named the field 'organizations' (plural)
    organizations = models.ForeignKey(
        "organizations.Organization", 
        on_delete=models.CASCADE, 
        related_name='placements',
        null=True,
        blank=True
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    workplace_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='workplace_placements'
    )
    
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
    final_report = models.FileField(upload_to='reports/', null=True, blank=True)
    report_submitted_at = models.DateTimeField(null=True, blank=True)
    grade = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        # We check if organizations exists first
        org_name = self.organizations.name if self.organizations else "No Organization"
        
        # Accessing student -> user -> username
        student_name = self.student.user.username if self.student and self.student.user else "Unknown Student"
        
        return f"{student_name} at {org_name}"
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



    def save(self, *args, **kwargs):
        if not self.pk:  # Only do this when a NEW log is created
            # Find the highest week number already submitted for THIS placement
            last_log = WeeklyLog.objects.filter(placement=self.placement).order_by('-week_number').first()
            if last_log:
                self.week_number = last_log.week_number + 1
            else:
                self.week_number = 1  # First log ever
        super().save(*args, **kwargs) 
    
    # Separate feedback and verification
    workplace_feedback = models.TextField(blank=True, null=True)
    academic_feedback = models.TextField(blank=True, null=True)
    
    is_verified_by_workplace = models.BooleanField(default=False)    