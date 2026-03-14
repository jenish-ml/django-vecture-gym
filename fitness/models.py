from django.db import models
from accounts.models import User

class GymGoal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class NutritionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    plan_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_workouts', limit_choices_to={'role': 'trainer'})
    week_start_date = models.DateField()
    day_1_plan = models.TextField(blank=True, null=True)
    day_2_plan = models.TextField(blank=True, null=True)
    day_3_plan = models.TextField(blank=True, null=True)
    day_4_plan = models.TextField(blank=True, null=True)
    day_5_plan = models.TextField(blank=True, null=True)
    day_6_plan = models.TextField(blank=True, null=True)
    day_7_plan = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.member.username} - Week of {self.week_start_date}"

class DietPlan(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_plans')
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_diets', limit_choices_to={'role': 'trainer'})
    duration_months = models.IntegerField(default=3)
    detailed_plan = models.TextField()

    def __str__(self):
        return f"{self.member.username} - Diet Plan"

class UserProgress(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_reports')
    date = models.DateField(auto_now_add=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Body Fat %")
    muscle_mass_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Muscle Mass in kg")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.member.username} - {self.date}"

class OnlineWorkoutPlan(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='online_workout_plans', limit_choices_to={'role': 'member', 'member_type': 'online'})
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_online_workouts', limit_choices_to={'role': 'trainer'})
    week_start_date = models.DateField()
    
    def __str__(self):
        return f"{self.member.username} - Online Workout - {self.week_start_date}"

class OnlineWorkoutSession(models.Model):
    DAY_CHOICES = [
        ('1', 'Day 1'), ('2', 'Day 2'), ('3', 'Day 3'), ('4', 'Day 4'),
        ('5', 'Day 5'), ('6', 'Day 6'), ('7', 'Day 7'),
    ]
    plan = models.ForeignKey(OnlineWorkoutPlan, on_delete=models.CASCADE, related_name='sessions')
    day_of_week = models.CharField(max_length=2, choices=DAY_CHOICES)
    time_slot = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True, help_text="Write notes with bullet points for easiest reading.")
    video_url = models.URLField(max_length=500, blank=True, null=True, help_text="Provide a YouTube embedded link (e.g. https://www.youtube.com/embed/...)")

    def get_embed_url(self):
        """Convert a regular YouTube URL to an embed URL."""
        if not self.video_url:
            return ''
        url = self.video_url
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return url

    def __str__(self):
        return f"{self.plan.member.username} - Day {self.day_of_week} - {self.title}"

class OnlineDietPlan(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='online_diet_plans', limit_choices_to={'role': 'member', 'member_type': 'online'})
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_online_diets', limit_choices_to={'role': 'trainer'})
    week_start_date = models.DateField()

    def __str__(self):
        return f"{self.member.username} - Online Diet - {self.week_start_date}"

class OnlineDietMeal(models.Model):
    DAY_CHOICES = [
        ('1', 'Day 1'), ('2', 'Day 2'), ('3', 'Day 3'), ('4', 'Day 4'),
        ('5', 'Day 5'), ('6', 'Day 6'), ('7', 'Day 7'),
    ]
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Snacks', 'Snacks'),
        ('Dinner', 'Dinner'),
    ]
    plan = models.ForeignKey(OnlineDietPlan, on_delete=models.CASCADE, related_name='meals')
    day_of_week = models.CharField(max_length=2, choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES)
    time_slot = models.TimeField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.plan.member.username} - Day {self.day_of_week} ({self.meal_type})"

class FeeTracking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    )
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fee_records', limit_choices_to={'role': 'member'})
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.member.username} - {self.due_date} - {self.status}"

class WorkoutVideo(models.Model):
    CATEGORY_CHOICES = [
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Shoulders', 'Shoulders'),
        ('Arms', 'Arms'),
        ('Legs', 'Legs'),
        ('Abs', 'Abs'),
        ('Cardio', 'Cardio'),
        ('Full Body', 'Full Body'),
        ('Stretching', 'Stretching'),
        ('Other', 'Other'),
    ]
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_videos', limit_choices_to={'role': 'trainer'})
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(max_length=500, help_text="Paste a YouTube URL (e.g. https://www.youtube.com/watch?v=... or https://www.youtube.com/embed/...)")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_embed_url(self):
        """Convert a regular YouTube URL to an embed URL."""
        url = self.video_url
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return url  # Already an embed URL or other format

    def __str__(self):
        return f"{self.title} by {self.trainer.username}"

