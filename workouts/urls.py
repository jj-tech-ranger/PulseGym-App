from django.urls import path
from .views import CategoryListView, VideoPlayerView, ToggleBookmarkView

app_name = 'workouts'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('exercise/<int:pk>/', VideoPlayerView.as_view(), name='video_player'),
    path('exercise/<int:pk>/bookmark/', ToggleBookmarkView.as_view(), name='toggle_bookmark'),
]
