from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Category, Exercise, Bookmark


class CategoryListView(LoginRequiredMixin, ListView):
    """Display workout categories, grouped by level."""
    model = Category
    template_name = 'workouts/category_list.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Defer loading the 'description' (NCLOB) field to prevent the ORA-00932 error on grouping.
        categories_with_calories = Category.objects.defer("description").annotate(
            total_calories=Sum('exercises__calories_burned')
        ).prefetch_related('exercises')

        # Group categories by level
        context['grouped_categories'] = {
            'beginner': categories_with_calories.filter(level='beginner'),
            'intermediate': categories_with_calories.filter(level='intermediate'),
            'advanced': categories_with_calories.filter(level='advanced'),
        }
        return context


class VideoPlayerView(LoginRequiredMixin, DetailView):
    """Display exercise video player."""
    model = Exercise
    template_name = 'workouts/video_player.html'
    context_object_name = 'exercise'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_bookmarked'] = Bookmark.objects.filter(
                user=self.request.user,
                exercise=self.object
            ).exists()
        return context


class ToggleBookmarkView(LoginRequiredMixin, View):
    """Toggle bookmark for an exercise."""
    login_url = reverse_lazy('accounts:login')
    
    def post(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            exercise=exercise
        )
        
        if not created:
            bookmark.delete()
            return JsonResponse({'status': 'removed', 'bookmarked': False})
        
        return JsonResponse({'status': 'added', 'bookmarked': True})
