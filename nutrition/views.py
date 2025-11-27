from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Meal

class DailyView(LoginRequiredMixin, TemplateView):
    template_name = 'nutrition/daily_view.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all meals and their related meal plan to access the plan's name
        all_meals = Meal.objects.select_related('meal_plan').all()
        
        # Group meals by their type for the tabbed view
        context['grouped_meals'] = {
            'breakfast': all_meals.filter(meal_type='breakfast'),
            'lunch': all_meals.filter(meal_type='lunch'),
            'dinner': all_meals.filter(meal_type='dinner'),
        }
        return context
