   
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

    email =models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# --- Profile Models ---

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.CharField(max_length=50, unique=True)
    course = models.CharField(max_length=100)
    year_of_study = models.PositiveIntegerField()
    is_eligible=models.BooleanField(default=False)
    cv=models.FileField(upload_to='cvs/', null=True , blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.registration_number}"
    
class WorkplaceSupervisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='workplace_profile')
    # This will link to the Organization model we create next
    organizations= models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='supervisors', null=True)
    job_title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.job_title})"


class AcademicSupervisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='academic_profile')
    department = models.CharField(max_length=100)
    


    def __str__(self):
        return self.user.get_full_name()