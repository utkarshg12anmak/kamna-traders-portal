# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    job_title = models.CharField("Job Title", max_length=100, blank=True)
