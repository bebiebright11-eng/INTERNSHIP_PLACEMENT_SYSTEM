from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile, AcademicSupervisorProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            StudentProfile.objects.create(user=instance)
        elif instance.role == 'academic_sup':
            AcademicSupervisorProfile.objects.create(user=instance)