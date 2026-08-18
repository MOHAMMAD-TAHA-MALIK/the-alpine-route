from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    @property
    def is_full(self):
        return self.participants.count() >= self.max_participants

    def __str__(self):
        return f"{self.title} ({self.date})"


class TrekEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='treks/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='trek_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_past(self):
        return self.date < timezone.now().date()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.title} ({self.date})"


class Comment(models.Model):
    trek = models.ForeignKey(TrekEvent, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.trek.title}"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"