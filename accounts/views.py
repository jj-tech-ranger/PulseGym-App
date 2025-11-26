from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import User, Profile
from .forms import PulseSignupForm, OnboardingFormStep1, OnboardingFormStep2, OnboardingFormStep3, OnboardingFormStep4


class PulseLoginView(LoginView):
    """Custom login view with PulseGym styling"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)


class PulseLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('login')


class SignUpView(CreateView):
    """User registration view"""
    model = User
    form_class = PulseSignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('onboarding_gender')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        # Create profile for new user
        Profile.objects.create(user=self.object)
        messages.success(self.request, 'Welcome to PulseGym!')
        return response


class OnboardingGenderView(LoginRequiredMixin, View):
    """Onboarding step 1: Gender selection"""
    template_name = 'accounts/wizard_gender.html'
    
    def get(self, request):
        form = OnboardingFormStep1(instance=request.user.profile)
        return render(request, self.template_name, {'form': form, 'step': 1})
    
    def post(self, request):
        form = OnboardingFormStep1(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('onboarding_age')
        return render(request, self.template_name, {'form': form, 'step': 1})


class OnboardingAgeView(LoginRequiredMixin, View):
    """Onboarding step 2: Age selection"""
    template_name = 'accounts/wizard_age.html'
    
    def get(self, request):
        form = OnboardingFormStep2(instance=request.user.profile)
        return render(request, self.template_name, {'form': form, 'step': 2})
    
    def post(self, request):
        form = OnboardingFormStep2(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('onboarding_metrics')
        return render(request, self.template_name, {'form': form, 'step': 2})


class OnboardingMetricsView(LoginRequiredMixin, View):
    """Onboarding step 3: Height and weight"""
    template_name = 'accounts/wizard_metrics.html'
    
    def get(self, request):
        form = OnboardingFormStep3(instance=request.user.profile)
        return render(request, self.template_name, {'form': form, 'step': 3})
    
    def post(self, request):
        form = OnboardingFormStep3(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('onboarding_goal')
        return render(request, self.template_name, {'form': form, 'step': 3})


class OnboardingGoalView(LoginRequiredMixin, View):
    """Onboarding step 4: Fitness goal selection"""
    template_name = 'accounts/wizard_goal.html'
    
    def get(self, request):
        form = OnboardingFormStep4(instance=request.user.profile)
        return render(request, self.template_name, {'form': form, 'step': 4})
    
    def post(self, request):
        form = OnboardingFormStep4(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile setup complete!')
            return redirect('home')
        return render(request, self.template_name, {'form': form, 'step': 4})


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile display view"""
    template_name = 'accounts/profile_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context


class ProfileEditView(LoginRequiredMixin, View):
    """Edit user profile"""
    template_name = 'accounts/profile_edit.html'
    
    def get(self, request):
        return render(request, self.template_name, {'profile': request.user.profile})
    
    def post(self, request):
        profile = request.user.profile
        profile.age = request.POST.get('age', profile.age)
        profile.weight = request.POST.get('weight', profile.weight)
        profile.height = request.POST.get('height', profile.height)
        profile.activity_level = request.POST.get('activity_level', profile.activity_level)
        profile.goal = request.POST.get('goal', profile.goal)
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
