from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Trek(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='moderate')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_treks')
    participants = models.ManyToManyField(User, related_name='joined_treks', blank=True)

    def __str__(self):
        return f"{self.title} ({self.date})"
