from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MealPlan, Meal

class DailyView(LoginRequiredMixin, TemplateView):
    template_name = 'nutrition/daily_view.html'
    login_url = 'accounts:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal_plan = MealPlan.objects.first()
        if meal_plan:
            context['meal_plan'] = meal_plan
            context['meals'] = {
                'breakfast': meal_plan.meals.filter(meal_type='breakfast'),
                'lunch': meal_plan.meals.filter(meal_type='lunch'),
                'dinner': meal_plan.meals.filter(meal_type='dinner'),
            }
        return context
