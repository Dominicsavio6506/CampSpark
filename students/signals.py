from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student
from academics.models import Department


@receiver(post_save, sender=User)
def create_student_for_user(sender, instance, created, **kwargs):

    if created and not instance.is_superuser:

        if not Student.objects.filter(user=instance).exists():

            dept = Department.objects.first()

            Student.objects.create(
                user=instance,
                name=instance.username,
                roll_number=f"AUTO-{instance.id}",
                year=1,
                department_fk=dept if dept else None
            )