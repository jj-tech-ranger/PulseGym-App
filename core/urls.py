from django.urls import path
from .views import HomeView, ProgressView, OffersView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('progress/', ProgressView.as_view(), name='progress'),
    path('offers/', OffersView.as_view(), name='offers'),
]
