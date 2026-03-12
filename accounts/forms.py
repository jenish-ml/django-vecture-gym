from django import forms
from .models import User, UserProfile
from fitness.models import GymGoal, MembershipPlan, NutritionPlan


class NoHelpTextMixin:
    """Mixin that removes help_text from all form fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''


class RegistrationForm(NoHelpTextMixin, forms.ModelForm):
    MEMBER_TYPE_CHOICES = (
        ('', 'Select Member Type'),
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    member_type = forms.ChoiceField(choices=MEMBER_TYPE_CHOICES, required=True)
    
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone_no = forms.CharField(required=False)
    
    # Profile fields
    fitness_goal = forms.ModelChoiceField(queryset=GymGoal.objects.all(), required=False)
    trainer = forms.ModelChoiceField(queryset=User.objects.filter(role='trainer'), required=False)
    membership_plan = forms.ModelChoiceField(queryset=MembershipPlan.objects.all(), required=False)
    nutrition_plan = forms.ModelChoiceField(queryset=NutritionPlan.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_no', 'member_type']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
            
        member_type = cleaned_data.get('member_type')
        
        if not member_type:
            self.add_error('member_type', 'Member type is required.')
        
        return cleaned_data


class LoginForm(NoHelpTextMixin, forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
