from django.contrib import admin
from .models import GymGoal, MembershipPlan, NutritionPlan, WorkoutPlan, DietPlan, UserProgress

admin.site.register(GymGoal)
admin.site.register(MembershipPlan)
admin.site.register(NutritionPlan)
admin.site.register(WorkoutPlan)
admin.site.register(DietPlan)
admin.site.register(UserProgress)
