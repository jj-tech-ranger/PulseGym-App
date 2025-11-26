from django.db import models
from django.conf import settings


class Category(models.Model):
    """Workout category model (Beginner/Intermediate/Advanced)."""
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['level', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Exercise(models.Model):
    """Exercise model with video content."""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    video_url = models.URLField(blank=True)
    thumbnail = models.URLField(blank=True)
    calories_burned = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'title']
    
    def __str__(self):
        return self.title


class Bookmark(models.Model):
    """User bookmark for exercises."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'exercise']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.exercise.title}"
