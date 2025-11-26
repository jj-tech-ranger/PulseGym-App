from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Category, Exercise, Bookmark


class CategoryListView(LoginRequiredMixin, ListView):
    """Display workout categories."""
    model = Category
    template_name = 'workouts/category_list.html'
    context_object_name = 'categories'
    login_url = 'accounts:login'
    
    def get_queryset(self):
        return Category.objects.prefetch_related('exercises')


class VideoPlayerView(LoginRequiredMixin, DetailView):
    """Display exercise video player."""
    model = Exercise
    template_name = 'workouts/video_player.html'
    context_object_name = 'exercise'
    login_url = 'accounts:login'
    
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
    login_url = 'accounts:login'
    
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
