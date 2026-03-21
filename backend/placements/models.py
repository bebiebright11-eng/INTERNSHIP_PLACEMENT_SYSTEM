from django.db import models
from django.conf import settings
from organizations.models import Organization

class InternshipPlacement(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    # settings.AUTH_USER_MODEL ensures we point to your custom User in accounts
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='placement'
    )
    organizations = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name='placements'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Workplace Supervisor is often a plain name initially, 
    # but Academic Supervisor must be a User with the correct role.
    workplace_supervisor = models.CharField(max_length=255, blank=True)
    academic_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='academic_students',
        limit_choices_to={'role': 'academic_sup'} # Only shows academic supervisors in Admin
    )

    final_score = models.IntegerField(null=True, blank=True)
    final_evaluation_comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} at {self.organization.name}"

class WeeklyLog(models.Model):
    placement = models.ForeignKey(
        InternshipPlacement, 
        on_delete=models.CASCADE, 
        related_name='logs'
    )
    week_number = models.PositiveIntegerField()
    tasks_performed = models.TextField()
    challenges = models.TextField(blank=True)
    attendance_days = models.PositiveIntegerField(default=5)
    
    supervisor_feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Week {self.week_number} - {self.placement.student.username}"