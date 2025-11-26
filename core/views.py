from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    """Home dashboard view with 4-block grid."""
    template_name = 'core/home.html'
    login_url = 'accounts:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_blocks'] = [
            {
                'title': 'Workouts',
                'icon': 'dumbbell',
                'url': 'workouts:category_list',
                'description': 'Browse workout categories',
                'color': 'primary'
            },
            {
                'title': 'Nutrition',
                'icon': 'utensils',
                'url': 'nutrition:daily_view',
                'description': 'View meal plans',
                'color': 'secondary'
            },
            {
                'title': 'Progress',
                'icon': 'chart-line',
                'url': '#',
                'description': 'Track your progress',
                'color': 'primary'
            },
            {
                'title': 'Offers',
                'icon': 'gift',
                'url': '#',
                'description': 'Special offers',
                'color': 'secondary'
            }
        ]
        return context
