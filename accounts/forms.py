from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class PulseSignupForm(UserCreationForm):
    """Custom signup form for PulseGym"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the default email field to make it required and styled
        self.fields['email'] = forms.EmailField(
            required=True,
            widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email'})
        )
        # Update password field placeholders
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set username to be the same as the email
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class OnboardingFormStep1(forms.ModelForm):
    """Onboarding step 1: Gender selection"""
    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'gender-radio'})
    )

    class Meta:
        model = Profile
        fields = ['gender']


class OnboardingFormStep2(forms.ModelForm):
    """Onboarding step 2: Age selection"""
    age = forms.IntegerField(
        min_value=13,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'age-slider',
            'type': 'range',
            'min': '13',
            'max': '100',
            'value': '25'
        })
    )

    class Meta:
        model = Profile
        fields = ['age']


class OnboardingFormStep3(forms.ModelForm):
    """Onboarding step 3: Height and weight metrics"""
    height = forms.IntegerField(
        min_value=100,
        max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'metric-slider',
            'type': 'range',
            'min': '100',
            'max': '250',
            'value': '170'
        }),
        help_text='Height in cm'
    )
    weight = forms.IntegerField(
        min_value=30,
        max_value=200,
        widget=forms.NumberInput(attrs={
            'class': 'metric-slider',
            'type': 'range',
            'min': '30',
            'max': '200',
            'value': '70'
        }),
        help_text='Weight in kg'
    )

    class Meta:
        model = Profile
        fields = ['height', 'weight']


class OnboardingFormStep4(forms.ModelForm):
    """Onboarding step 4: Fitness goal selection"""
    goal = forms.ChoiceField(
        choices=Profile.GOAL_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'goal-radio'})
    )
    activity_level = forms.ChoiceField(
        choices=Profile.ACTIVITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Profile
        fields = ['goal', 'activity_level']
