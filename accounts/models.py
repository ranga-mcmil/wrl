from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField


class User(AbstractUser):

    class Types(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        SUPERVISOR = "SUPERVISOR", 'Supervisor'
        WORK_SUPERVISOR = "WORK_SUPERVISOR", "Work_Supervisor"

    # Type of user
    type = models.CharField(_('Type'), max_length=50, choices=Types.choices) # default=Types.STUDENT
    pic = ResizedImageField(size=[500, 500], crop=['top', 'left'], upload_to='images/', blank=True, null=True)


    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})



# class DoctorManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset(*args, **kwargs).filter(type=User.Types.DOCTOR)


class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager, self).get_queryset().filter(type=User.Types.STUDENT)

class SupervisorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SUPERVISOR)

class WorkSupervisorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.WORK_SUPERVISOR)




class Supervisor(User):
    objects = SupervisorManager()

    class Meta:
        proxy = True

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.SUPERVISOR
        return super().save(*args, **kwargs)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
        return super().save(*args, **kwargs)


class WorkSupervisor(User):
    objects = WorkSupervisorManager()

    class Meta:
        proxy = True

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.WORK_SUPERVISOR
        return super().save(*args, **kwargs)


# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    programme = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'

class Contact(models.Model):
    user_from = models.ForeignKey(User,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} is supervising {self.user_to}'



# # Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('supervising',
                       models.ManyToManyField('self',
                           through=Contact,
                           related_name='supervised_by',
                           symmetrical=False))