from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('member', 'Member'),
    )
    MEMBER_TYPE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fitness_goal = models.ForeignKey('fitness.GymGoal', on_delete=models.SET_NULL, null=True, blank=True)
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainees', limit_choices_to={'role': 'trainer'})
    membership_plan = models.ForeignKey('fitness.MembershipPlan', on_delete=models.SET_NULL, null=True, blank=True)
    nutrition_plan = models.ForeignKey('fitness.NutritionPlan', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
