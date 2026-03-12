from django import forms
from accounts.models import User, UserProfile
from shop.models import Product, Category
from fitness.models import GymGoal, MembershipPlan, NutritionPlan, WorkoutPlan, DietPlan, FeeTracking


class NoHelpTextMixin:
    """Mixin that removes help_text from all form fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''


class CategoryForm(NoHelpTextMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class AdminUserForm(NoHelpTextMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_no', 'role', 'member_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AdminTrainerForm(NoHelpTextMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    image = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_no']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'trainer'
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ProductForm(NoHelpTextMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image', 'is_active']

class MembershipPlanForm(NoHelpTextMixin, forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ['name', 'price', 'duration_months', 'description']

class NutritionPlanForm(NoHelpTextMixin, forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = ['name', 'description']

class GymGoalForm(NoHelpTextMixin, forms.ModelForm):
    class Meta:
        model = GymGoal
        fields = ['name', 'description']

class WorkoutPlanForm(NoHelpTextMixin, forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['member', 'week_start_date', 'day_1_plan', 'day_2_plan', 'day_3_plan', 'day_4_plan', 'day_5_plan', 'day_6_plan', 'day_7_plan']
        widgets = {
            'week_start_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        super().__init__(*args, **kwargs)
        if trainer:
            self.fields['member'].queryset = User.objects.filter(profile__trainer=trainer)
        for field in self.fields.values():
            field.help_text = ''

class DietPlanForm(NoHelpTextMixin, forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ['member', 'duration_months', 'detailed_plan']

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        super().__init__(*args, **kwargs)
        if trainer:
            self.fields['member'].queryset = User.objects.filter(profile__trainer=trainer)
        for field in self.fields.values():
            field.help_text = ''

class FeeTrackingForm(NoHelpTextMixin, forms.ModelForm):
    class Meta:
        model = FeeTracking
        fields = ['member', 'membership_plan', 'amount_due', 'amount_paid', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

from fitness.models import OnlineWorkoutPlan, OnlineWorkoutSession, OnlineDietPlan, OnlineDietMeal

class OnlineWorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = OnlineWorkoutPlan
        fields = ['member', 'week_start_date']
        widgets = {
            'week_start_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        super().__init__(*args, **kwargs)
        if trainer:
            self.fields['member'].queryset = User.objects.filter(profile__trainer=trainer, member_type='online')

class OnlineWorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = OnlineWorkoutSession
        fields = ['day_of_week', 'time_slot', 'title', 'notes', 'video']
        widgets = {
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write notes with bullet points for easiest reading...'}),
        }

class OnlineDietPlanForm(forms.ModelForm):
    class Meta:
        model = OnlineDietPlan
        fields = ['member', 'week_start_date']
        widgets = {
            'week_start_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        super().__init__(*args, **kwargs)
        if trainer:
            self.fields['member'].queryset = User.objects.filter(profile__trainer=trainer, member_type='online')

class OnlineDietMealForm(forms.ModelForm):
    class Meta:
        model = OnlineDietMeal
        fields = ['day_of_week', 'meal_type', 'time_slot', 'description']
        widgets = {
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
