from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from workouts.models import Bookmark
from accounts.models import WeightEntry
import json

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_blocks'] = [
            {'title': 'Workouts', 'icon': 'dumbbell', 'url': 'workouts:category_list', 'description': 'Browse workout categories', 'color': 'primary'},
            {'title': 'Nutrition', 'icon': 'utensils', 'url': 'nutrition:daily_view', 'description': 'View meal plans', 'color': 'secondary'},
            {'title': 'Progress', 'icon': 'chart-line', 'url': 'core:progress', 'description': 'Track your progress', 'color': 'primary'},
            {'title': 'Offers', 'icon': 'gift', 'url': 'core:offers', 'description': 'Special offers', 'color': 'secondary'}
        ]
        return context

class ProgressView(LoginRequiredMixin, TemplateView):
    template_name = 'core/progress.html'
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Weight data for the chart
        weight_entries = WeightEntry.objects.filter(user=user).order_by('date_recorded')
        context['weight_dates'] = json.dumps([entry.date_recorded.strftime('%b %d') for entry in weight_entries])
        context['weight_values'] = json.dumps([entry.weight for entry in weight_entries])
        
        # Other stats
        context['profile'] = user.profile
        context['bookmarked_exercises'] = Bookmark.objects.filter(user=user).select_related('exercise')
        context['latest_weight'] = weight_entries.last().weight if weight_entries else user.profile.weight
        context['start_weight'] = weight_entries.first().weight if weight_entries else user.profile.weight
        
        return context

    def post(self, request, *args, **kwargs):
        try:
            weight = float(request.POST.get('weight'))
            if weight > 0:
                WeightEntry.objects.create(user=request.user, weight=weight, date_recorded=timezone.now().date())
                messages.success(request, 'Weight entry added successfully!')
            else:
                messages.error(request, 'Please enter a valid weight.')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid input. Please enter a number for the weight.')
        
        return redirect('core:progress')


class OffersView(LoginRequiredMixin, TemplateView):
    template_name = 'core/offers.html'
    login_url = reverse_lazy('accounts:login')
