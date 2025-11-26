from django.contrib import admin
from .models import Category, Exercise, Bookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'created_at')
    list_filter = ('level',)
    search_fields = ('name',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'calories_burned')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'created_at')
    list_filter = ('created_at',)
