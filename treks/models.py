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





class TrekEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='treks/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='trek_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    trek = models.ForeignKey(TrekEvent, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.trek.title}"