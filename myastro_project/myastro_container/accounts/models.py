from django.db import models
from django.contrib.auth.models import AbstractUser


class PersonBase(models.Model):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_hour = models.IntegerField(blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class User(AbstractUser, PersonBase):
    pass


   
