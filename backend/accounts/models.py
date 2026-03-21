   
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Internship Administrator'),
        ('workplace_sup', 'Workplace Supervisor'),
        ('academic_sup', 'Academic Supervisor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# --- Profile Models ---

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.CharField(max_length=50, unique=True)
    course = models.CharField(max_length=100)
    year_of_study = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

class AcademicSupervisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='academic_profile')
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()