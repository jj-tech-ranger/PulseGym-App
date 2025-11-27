from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.PulseLoginView.as_view(), name='login'),
    path('logout/', views.PulseLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    # Onboarding wizard
    path('onboarding/gender/', views.OnboardingGenderView.as_view(), name='onboarding_gender'),
    path('onboarding/age/', views.OnboardingAgeView.as_view(), name='onboarding_age'),
    path('onboarding/metrics/', views.OnboardingMetricsView.as_view(), name='onboarding_metrics'),
    path('onboarding/goal/', views.OnboardingGoalView.as_view(), name='onboarding_goal'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]
