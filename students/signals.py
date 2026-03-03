from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student, Department

@receiver(post_save, sender=User)
def create_student_for_user(sender, instance, created, **kwargs):
    # Do NOT create Student for admin/superuser
    if created and not instance.is_superuser:
        dept = Department.objects.first()

        Student.objects.create(
            user=instance,
            name=instance.username,
            roll_number=f"AUTO-{instance.id}",
            year=1,
            department=dept
        )
