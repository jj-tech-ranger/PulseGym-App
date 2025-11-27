from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'accounts_user'

class Profile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('active', 'Very Active'),
    ]
    GOAL_CHOICES = [
        ('lose', 'Lose Weight'),
        ('gain', 'Gain Muscle'),
        ('maintain', 'Maintain Weight'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        db_table = 'accounts_profile'

class WeightEntry(models.Model):
    """Stores a user's weight at a specific point in time."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_entries')
    weight = models.FloatField()
    date_recorded = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['date_recorded']
        verbose_name_plural = 'Weight Entries'

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg on {self.date_recorded}"
