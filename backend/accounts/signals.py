from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile, AcademicSupervisorProfile,WorkplaceSupervisorProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            StudentProfile.objects.create(user=instance,year_of_study=1)
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.role == 'academic_sup':
            AcademicSupervisorProfile.objects.create(user=instance)
        elif instance.role == 'workplace_sup':
            WorkplaceSupervisorProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'student' and hasattr(instance, 'student_profile'):
        instance.student_profile.save()
    elif instance.role == 'academic_sup' and hasattr(instance, 'academic_profile'):
        instance.academic_profile.save()
    elif instance.role == 'workplace_sup' and hasattr(instance, 'workplace_profile'):
        instance.workplace_profile.save()