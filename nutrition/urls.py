from django.urls import path
from .views import DailyView

app_name = 'nutrition'

urlpatterns = [
    path('', DailyView.as_view(), name='daily_view'),
]
