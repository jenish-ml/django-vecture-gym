"""
Django management command to flush all data and seed the database
with realistic sample data for the Vecture Gym Management project.

Usage:
    python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta, time
import decimal


class Command(BaseCommand):
    help = 'Flush all data and seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('⚠  Flushing all existing data...'))
        self._flush()
        self.stdout.write(self.style.SUCCESS('✓  Database cleared.'))

        self.stdout.write('  Seeding sample data...')
        self._seed_goals()
        self._seed_membership_plans()
        self._seed_nutrition_plans()
        self._seed_categories_and_products()
        self._seed_users()
        self._seed_fees()
        self._seed_workout_diet_plans()
        self._seed_online_plans()
        self._seed_progress()
        self._seed_orders()
        self._seed_contact_messages()

        self.stdout.write(self.style.SUCCESS('\n✅  All sample data seeded successfully!\n'))
        self.stdout.write(self.style.SUCCESS('  Login Credentials:'))
        self.stdout.write('  Admin   → username: admin        | password: admin123')
        self.stdout.write('  Trainer → username: raj_trainer  | password: trainer123')
        self.stdout.write('  Trainer → username: priya_trainer | password: trainer123')
        self.stdout.write('  Member  → username: arjun_online  | password: member123  (Online)')
        self.stdout.write('  Member  → username: sunita_online  | password: member123  (Online)')
        self.stdout.write('  Member  → username: ramesh_offline | password: member123  (Offline)')
        self.stdout.write('  Member  → username: kavya_offline  | password: member123  (Offline)')

    # ───────────────────────────────────────────────────────────────────────────
    def _flush(self):
        from django.db import connection
        from django.apps import apps

        # Order matters for FK constraints
        models_to_clear = [
            'fitness.OnlineDietMeal', 'fitness.OnlineDietPlan',
            'fitness.OnlineWorkoutSession', 'fitness.OnlineWorkoutPlan',
            'fitness.UserProgress', 'fitness.DietPlan', 'fitness.WorkoutPlan',
            'fitness.FeeTracking',
            'shop.CartItem', 'shop.Cart', 'shop.OrderItem', 'shop.Order',
            'shop.Product', 'shop.Category',
            'core.ContactMessage',
            'accounts.UserProfile',
            'fitness.NutritionPlan', 'fitness.MembershipPlan', 'fitness.GymGoal',
            'accounts.User',
        ]
        for label in models_to_clear:
            app, model = label.split('.')
            Model = apps.get_model(app, model)
            Model.objects.all().delete()

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_goals(self):
        from fitness.models import GymGoal
        goals = [
            ('Weight Loss', 'Reduce body fat and achieve a healthy BMI.'),
            ('Muscle Gain', 'Build lean muscle mass through progressive overload.'),
            ('General Fitness', 'Improve overall stamina, strength, and flexibility.'),
            ('Athletic Performance', 'Enhance speed, agility, and endurance for sports.'),
            ('Rehabilitation', 'Recover from injuries with guided low-impact exercises.'),
        ]
        for name, desc in goals:
            GymGoal.objects.create(name=name, description=desc)
        self.stdout.write('  ✓ Gym Goals')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_membership_plans(self):
        from fitness.models import MembershipPlan
        plans = [
            ('Silver Plan', 999,  1, 'Basic access to gym equipment and locker room.'),
            ('Gold Plan',   1999, 3, 'Full access including group classes and sauna.'),
            ('Platinum Plan', 3499, 6, 'All access including personal trainer sessions and diet consultation.'),
            ('Annual Plan',  5999, 12, 'Best value annual membership with all premium benefits.'),
        ]
        for name, price, months, desc in plans:
            MembershipPlan.objects.create(
                name=name, price=decimal.Decimal(price),
                duration_months=months, description=desc
            )
        self.stdout.write('  ✓ Membership Plans')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_nutrition_plans(self):
        from fitness.models import NutritionPlan
        plans = [
            (
                'Weight Loss Diet',
                'Calorie-controlled plan focusing on lean proteins and vegetables.',
                '• Breakfast: Oats with skim milk and fruits\n'
                '• Mid-morning: Green tea + 10 almonds\n'
                '• Lunch: Grilled chicken 150g + brown rice + salad\n'
                '• Evening: Sprouts chaat\n'
                '• Dinner: Dal + 2 chapati + sabzi\n'
                '• Avoid: Fried foods, sweets, sugary drinks',
            ),
            (
                'Muscle Building Diet',
                'High-protein, high-calorie plan to support muscle hypertrophy.',
                '• Breakfast: 4 egg whites + 2 whole eggs + whole wheat toast\n'
                '• Mid-morning: Protein shake + banana\n'
                '• Lunch: Paneer/chicken 200g + rice + dal + sabzi\n'
                '• Pre-workout: Banana + peanut butter\n'
                '• Post-workout: Whey protein + milk\n'
                '• Dinner: Fish/chicken + sweet potato + broccoli',
            ),
            (
                'General Wellness Diet',
                'Balanced macro plan for maintaining health and energy.',
                '• Breakfast: Idli/dosa + sambar + coconut chutney\n'
                '• Mid-morning: Seasonal fruit\n'
                '• Lunch: Rice + dal + 2 sabzis + curd\n'
                '• Evening: Makhana or roasted chana\n'
                '• Dinner: Chapati + sabzi + dal',
            ),
        ]
        for name, desc, details in plans:
            NutritionPlan.objects.create(name=name, description=desc, plan_details=details)
        self.stdout.write('  ✓ Nutrition Plans')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_categories_and_products(self):
        from shop.models import Category, Product
        cats = {}
        for name in ['Supplements', 'Gym Equipment', 'Apparel', 'Accessories']:
            cats[name] = Category.objects.create(name=name)

        products = [
            # (name, category, description, price)
            ('Whey Protein 1kg', 'Supplements', 'Premium whey protein isolate – chocolate flavour. 25g protein per serve.', 1499),
            ('Creatine Monohydrate', 'Supplements', 'Pure micronised creatine for strength and power. 300g tub.', 799),
            ('BCAA 200g', 'Supplements', 'Branched-chain amino acids for recovery. Watermelon flavour.', 649),
            ('Multivitamin Pack (30 days)', 'Supplements', 'Daily multivitamin with vitamin D, B12, zinc, and magnesium.', 349),
            ('Adjustable Dumbbell Set', 'Gym Equipment', 'Pair of adjustable dumbbells 5–30kg. Space-saving design.', 8999),
            ('Resistance Bands Set', 'Gym Equipment', '5-band set with varying resistance levels for home workouts.', 499),
            ('Yoga Mat (6mm)', 'Gym Equipment', 'Non-slip TPE yoga mat with carrying strap.', 699),
            ('Jump Rope – Speed Skipping', 'Gym Equipment', 'Ball bearing speed rope with adjustable length.', 299),
            ('Gym T-Shirt – Dry-Fit', 'Apparel', 'Moisture-wicking dry-fit training tee. Sizes S–XXL.', 499),
            ('Compression Shorts', 'Apparel', 'High-performance compression shorts for training and recovery.', 799),
            ('Gym Gloves', 'Accessories', 'Padded gym gloves for improved grip and wrist support.', 349),
            ('Shaker Bottle 700ml', 'Accessories', 'Leak-proof protein shaker with mixing ball. BPA-free.', 199),
            ('Gym Bag – 40L', 'Accessories', 'Spacious gym bag with shoe compartment and water bottle pocket.', 1299),
        ]
        for name, cat, desc, price in products:
            Product.objects.create(
                name=name, category=cats[cat],
                description=desc, price=decimal.Decimal(price), is_active=True
            )
        self.stdout.write('  ✓ Products & Categories')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_users(self):
        from accounts.models import User, UserProfile
        from fitness.models import GymGoal, MembershipPlan, NutritionPlan

        # Goals & plans
        weight_loss = GymGoal.objects.get(name='Weight Loss')
        muscle_gain = GymGoal.objects.get(name='Muscle Gain')
        general     = GymGoal.objects.get(name='General Fitness')
        athletic    = GymGoal.objects.get(name='Athletic Performance')

        silver   = MembershipPlan.objects.get(name='Silver Plan')
        gold     = MembershipPlan.objects.get(name='Gold Plan')
        platinum = MembershipPlan.objects.get(name='Platinum Plan')

        wl_diet  = NutritionPlan.objects.get(name='Weight Loss Diet')
        mb_diet  = NutritionPlan.objects.get(name='Muscle Building Diet')
        gw_diet  = NutritionPlan.objects.get(name='General Wellness Diet')

        # ── Admin ──────────────────────────────────────────────────────────────
        admin = User.objects.create_superuser(
            username='admin', email='admin@vecture.com',
            password='admin123', first_name='Admin', last_name='Vecture',
            role='admin', phone_no='9000000000'
        )
        UserProfile.objects.create(user=admin)

        # ── Trainers ───────────────────────────────────────────────────────────
        raj = User.objects.create_user(
            username='raj_trainer', email='raj@vecture.com',
            password='trainer123', first_name='Raj', last_name='Kumar',
            role='trainer', phone_no='9111111111'
        )
        UserProfile.objects.create(user=raj)

        priya = User.objects.create_user(
            username='priya_trainer', email='priya@vecture.com',
            password='trainer123', first_name='Priya', last_name='Sharma',
            role='trainer', phone_no='9222222222'
        )
        UserProfile.objects.create(user=priya)

        # ── Online Members ─────────────────────────────────────────────────────
        arjun = User.objects.create_user(
            username='arjun_online', email='arjun@example.com',
            password='member123', first_name='Arjun', last_name='Mehta',
            role='member', member_type='online', phone_no='9333333333'
        )
        UserProfile.objects.create(
            user=arjun, trainer=raj,
            fitness_goal=weight_loss
        )

        sunita = User.objects.create_user(
            username='sunita_online', email='sunita@example.com',
            password='member123', first_name='Sunita', last_name='Patel',
            role='member', member_type='online', phone_no='9444444444'
        )
        UserProfile.objects.create(
            user=sunita, trainer=priya,
            fitness_goal=muscle_gain
        )

        # ── Offline Members ────────────────────────────────────────────────────
        ramesh = User.objects.create_user(
            username='ramesh_offline', email='ramesh@example.com',
            password='member123', first_name='Ramesh', last_name='Nair',
            role='member', member_type='offline', phone_no='9555555555'
        )
        UserProfile.objects.create(
            user=ramesh, trainer=raj,
            fitness_goal=general,
            membership_plan=gold,
            nutrition_plan=wl_diet
        )

        kavya = User.objects.create_user(
            username='kavya_offline', email='kavya@example.com',
            password='member123', first_name='Kavya', last_name='Reddy',
            role='member', member_type='offline', phone_no='9666666666'
        )
        UserProfile.objects.create(
            user=kavya, trainer=priya,
            fitness_goal=athletic,
            membership_plan=platinum,
            nutrition_plan=mb_diet
        )

        vikram = User.objects.create_user(
            username='vikram_offline', email='vikram@example.com',
            password='member123', first_name='Vikram', last_name='Singh',
            role='member', member_type='offline', phone_no='9777777777'
        )
        UserProfile.objects.create(
            user=vikram, trainer=raj,
            fitness_goal=muscle_gain,
            membership_plan=silver,
            nutrition_plan=mb_diet
        )

        self.stdout.write('  ✓ Users & Profiles')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_fees(self):
        from accounts.models import User
        from fitness.models import FeeTracking, MembershipPlan

        today = date.today()
        gold     = MembershipPlan.objects.get(name='Gold Plan')
        platinum = MembershipPlan.objects.get(name='Platinum Plan')
        silver   = MembershipPlan.objects.get(name='Silver Plan')

        fees = [
            # (username, plan, amount_due, amount_paid, due_date, status)
            ('ramesh_offline',  gold,     decimal.Decimal('1999'), decimal.Decimal('1999'), today - timedelta(days=30),  'Paid'),
            ('ramesh_offline',  gold,     decimal.Decimal('1999'), decimal.Decimal('0'),    today + timedelta(days=15),  'Pending'),
            ('kavya_offline',   platinum, decimal.Decimal('3499'), decimal.Decimal('3499'), today - timedelta(days=60),  'Paid'),
            ('kavya_offline',   platinum, decimal.Decimal('3499'), decimal.Decimal('0'),    today + timedelta(days=5),   'Pending'),
            ('vikram_offline',  silver,   decimal.Decimal('999'),  decimal.Decimal('0'),    today - timedelta(days=5),   'Overdue'),
            # Online members – normal fee (no membership plan required)
            ('arjun_online',    None,     decimal.Decimal('499'),  decimal.Decimal('499'),  today - timedelta(days=20),  'Paid'),
            ('arjun_online',    None,     decimal.Decimal('499'),  decimal.Decimal('0'),    today + timedelta(days=10),  'Pending'),
            ('sunita_online',   None,     decimal.Decimal('499'),  decimal.Decimal('0'),    today - timedelta(days=2),   'Overdue'),
        ]
        for username, plan, amount_due, amount_paid, due_date, status in fees:
            member = User.objects.get(username=username)
            FeeTracking.objects.create(
                member=member,
                membership_plan=plan,
                amount_due=amount_due,
                amount_paid=amount_paid,
                due_date=due_date,
                status=status
            )
        self.stdout.write('  ✓ Fee Records')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_workout_diet_plans(self):
        from accounts.models import User
        from fitness.models import WorkoutPlan, DietPlan

        today = date.today()
        raj    = User.objects.get(username='raj_trainer')
        priya  = User.objects.get(username='priya_trainer')
        ramesh = User.objects.get(username='ramesh_offline')
        kavya  = User.objects.get(username='kavya_offline')
        vikram = User.objects.get(username='vikram_offline')

        WorkoutPlan.objects.create(
            member=ramesh, trainer=raj,
            week_start_date=today - timedelta(days=today.weekday()),
            day_1_plan='Chest & Triceps: Bench Press 4x10, Incline Dumbbell Press 3x12, Tricep Dips 3x15, Cable Pushdown 3x15',
            day_2_plan='Back & Biceps: Pull-ups 4x8, Barbell Row 4x10, Lat Pulldown 3x12, Dumbbell Curls 3x15',
            day_3_plan='REST – Light walk 30 min, stretching',
            day_4_plan='Legs: Squat 4x10, Leg Press 3x12, Romanian Deadlift 3x12, Calf Raises 4x20',
            day_5_plan='Shoulders & Core: OHP 4x10, Lateral Raises 3x15, Face Pulls 3x15, Plank 3x60s',
            day_6_plan='Cardio: 5km run, 20 min cycling',
            day_7_plan='REST – Yoga / foam rolling',
        )

        WorkoutPlan.objects.create(
            member=kavya, trainer=priya,
            week_start_date=today - timedelta(days=today.weekday()),
            day_1_plan='Full Body Strength: Deadlift 4x5, Bench Press 4x8, Pull-ups 4x8',
            day_2_plan='Sprint Training: 10x50m sprints, box jumps 3x15',
            day_3_plan='REST + Mobility',
            day_4_plan='Lower Power: Squat 5x5, Jump Squats 3x10, Hip Thrusts 3x12',
            day_5_plan='Upper Hypertrophy: Arnold Press, Rows, Flyes',
            day_6_plan='HIIT 30 min',
            day_7_plan='REST',
        )

        WorkoutPlan.objects.create(
            member=vikram, trainer=raj,
            week_start_date=today - timedelta(days=today.weekday()),
            day_1_plan='Push: Bench 4x8, Overhead Press 4x8, Tricep Extensions 3x12',
            day_2_plan='Pull: Deadlift 4x6, Barbell Row 4x8, Face Pulls 3x15, Curls 3x12',
            day_3_plan='Legs: Squat 4x8, Lunges 3x12 each, Calf Raises 4x20',
            day_4_plan='REST',
            day_5_plan='Push again: Incline DB Press, Dips, Lateral Raises',
            day_6_plan='Pull again + Core: Pull-ups, Seated Rows, Planks',
            day_7_plan='REST',
        )

        # Diet plans for offline members
        DietPlan.objects.create(
            member=ramesh, trainer=raj, duration_months=3,
            detailed_plan=(
                'Breakfast (7:30 AM): 2 chapati + 2 boiled eggs + 200ml milk\n'
                'Mid-Morning (10:30 AM): 1 banana + 5 walnuts\n'
                'Lunch (1:00 PM): Brown rice 1 cup + dal + sabzi + curd\n'
                'Pre-Workout (4:00 PM): Banana + black coffee\n'
                'Post-Workout (6:30 PM): Whey shake + water\n'
                'Dinner (8:30 PM): 2 chapati + paneer sabzi + salad\n'
                '⚠ Avoid: Processed foods, sugary drinks, alcohol'
            )
        )

        DietPlan.objects.create(
            member=kavya, trainer=priya, duration_months=3,
            detailed_plan=(
                'Breakfast (6:00 AM): 4 egg whites omelette + oats + black coffee\n'
                'Mid-Morning (9:00 AM): Protein shake (25g protein)\n'
                'Lunch (1:00 PM): Grilled chicken 200g + sweet potato + salad\n'
                'Pre-Workout (4:30 PM): Rice cakes + peanut butter\n'
                'Post-Workout (7:00 PM): Whey protein 30g + milk\n'
                'Dinner (9:00 PM): Fish/chicken 150g + broccoli + quinoa\n'
                '⚠ Strict no junk, minimum 3 litres water daily'
            )
        )
        self.stdout.write('  ✓ Offline Workout & Diet Plans')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_online_plans(self):
        from accounts.models import User
        from fitness.models import OnlineWorkoutPlan, OnlineWorkoutSession, OnlineDietPlan, OnlineDietMeal

        today = date.today()
        week_start = today - timedelta(days=today.weekday())

        raj   = User.objects.get(username='raj_trainer')
        priya = User.objects.get(username='priya_trainer')
        arjun = User.objects.get(username='arjun_online')
        sunita = User.objects.get(username='sunita_online')

        # ── Arjun – Online Workout ─────────────────────────────────────────────
        arjun_wp = OnlineWorkoutPlan.objects.create(
            member=arjun, trainer=raj, week_start_date=week_start
        )
        sessions = [
            # (day, start_time, title, notes)
            ('1', time(6, 30), 'Chest & Triceps',
             '• Warm-up: 10 min jog\n• Push-ups 4x20\n• DB Bench Press 4x12\n• Incline DB Press 3x12\n• Tricep Dips 3x15\n• Cable Pushdown 3x15'),
            ('2', time(6, 30), 'Back & Biceps',
             '• Pull-ups 4x10\n• DB Bent Row 4x12\n• Lat Pulldown 3x12\n• Seated Row 3x12\n• DB Curls 3x15\n• Hammer Curls 3x15'),
            ('3', time(6, 0),  'Active Rest – Yoga',
             '• 30 min yoga flow\n• Focus on hip flexors and thoracic mobility'),
            ('4', time(6, 30), 'Legs – Quad Dominant',
             '• Squat 4x10\n• Leg Press 3x12\n• Lunges 3x12 each\n• Leg Extension 3x15\n• Calf Raises 4x20'),
            ('5', time(6, 30), 'Shoulders & Core',
             '• DB Overhead Press 4x12\n• Lateral Raises 3x15\n• Face Pulls 3x15\n• Plank 3×60s\n• Russian Twists 3x20\n• Hanging Leg Raises 3x12'),
            ('6', time(7, 0),  'HIIT Cardio',
             '• 5 min warm-up\n• 20 min HIIT: 40s work / 20s rest (burpees, high knees, mountain climbers)\n• 10 min cool-down'),
            ('7', None, 'Full Rest Day', '• No training\n• Focus on sleep and hydration'),
        ]
        for day, time_slot, title, notes in sessions:
            OnlineWorkoutSession.objects.create(
                plan=arjun_wp, day_of_week=day,
                time_slot=time_slot, title=title, notes=notes
            )

        # ── Arjun – Online Diet ────────────────────────────────────────────────
        arjun_dp = OnlineDietPlan.objects.create(
            member=arjun, trainer=raj, week_start_date=week_start
        )
        diet_meals = [
            # (day, meal_type, time_slot, description)
            ('1', 'Breakfast', time(7, 45),  'Oats 80g + skim milk 200ml + 1 banana + 10 almonds'),
            ('1', 'Lunch',     time(13, 0),  'Brown rice 1 cup + dal + chicken 150g + mixed sabzi + 1 curd'),
            ('1', 'Dinner',    time(20, 0),  '2 multigrain chapati + paneer bhurji + salad'),
            ('2', 'Breakfast', time(7, 45),  '3 egg whites + 1 whole egg scrambled + 2 whole wheat toast'),
            ('2', 'Lunch',     time(13, 0),  'Grilled chicken sandwich + green salad'),
            ('2', 'Dinner',    time(20, 0),  'Rice + rajma + sabzi'),
            ('3', 'Breakfast', time(7, 45),  'Poha + 1 boiled egg + green tea'),
            ('3', 'Lunch',     time(13, 0),  'Dal khichdi + curd + pickle'),
            ('3', 'Dinner',    time(20, 0),  '2 chapati + mixed veg sabzi + moong dal'),
            ('4', 'Breakfast', time(7, 45),  'Oats + protein powder + milk smoothie'),
            ('4', 'Lunch',     time(13, 0),  'Brown rice + dal + fish curry 150g'),
            ('4', 'Dinner',    time(20, 0),  '3 chapati + egg bhurji + salad'),
            ('5', 'Breakfast', time(7, 45),  'Idli 4 nos + sambar + coconut chutney'),
            ('5', 'Lunch',     time(13, 0),  'Rice + sambar + sabzi + curd'),
            ('5', 'Snacks',    time(17, 0),  'Sprouts chaat 100g + lemon water'),
            ('5', 'Dinner',    time(20, 0),  '2 chapati + dal + salad'),
            ('6', 'Breakfast', time(7, 0),   'Banana + peanut butter toast + black coffee'),
            ('6', 'Lunch',     time(13, 0),  'Chicken fried rice (home-made) + cucumber salad'),
            ('6', 'Dinner',    time(20, 0),  'Soup + 2 chapati + sabzi'),
            ('7', 'Breakfast', time(9, 0),   'Cheat meal: Aloo paratha + curd + pickle'),
            ('7', 'Lunch',     time(13, 30), 'Rice + dal makhani + sabzi + raita'),
            ('7', 'Dinner',    time(20, 0),  'Light khichdi + curd'),
        ]
        for day, meal_type, time_slot, description in diet_meals:
            OnlineDietMeal.objects.create(
                plan=arjun_dp, day_of_week=day,
                meal_type=meal_type, time_slot=time_slot,
                description=description
            )

        # ── Sunita – Online Workout ────────────────────────────────────────────
        sunita_wp = OnlineWorkoutPlan.objects.create(
            member=sunita, trainer=priya, week_start_date=week_start
        )
        sunita_sessions = [
            ('1', time(7, 0),  'Upper Body Strength',
             '• DB Press 4x10\n• DB Row 4x10\n• Shoulder Press 3x12\n• Bicep Curls 3x15\n• Tricep Kickbacks 3x15'),
            ('2', time(7, 0),  'Lower Body Strength',
             '• Goblet Squat 4x12\n• Romanian Deadlift 4x10\n• Hip Thrusts 4x15\n• Calf Raises 3x20'),
            ('3', time(7, 0),  'Core & Cardio',
             '• Plank 3x60s\n• 20 min steady-state cardio (walk/cycle)'),
            ('4', None, 'Rest', '• Rest day – light walk optional'),
            ('5', time(7, 0),  'Full Body Circuit',
             '• Squat to Press 3x12\n• Renegade Rows 3x10\n• Jump Squats 3x15\n• Push-ups 3x20'),
            ('6', time(7, 0),  'Cardio HIIT',
             '• 30 min HIIT session (bike/treadmill intervals)'),
            ('7', None, 'Rest', '• Rest and recovery'),
        ]
        for day, time_slot, title, notes in sunita_sessions:
            OnlineWorkoutSession.objects.create(
                plan=sunita_wp, day_of_week=day,
                time_slot=time_slot, title=title, notes=notes
            )

        # ── Sunita – Online Diet ───────────────────────────────────────────────
        sunita_dp = OnlineDietPlan.objects.create(
            member=sunita, trainer=priya, week_start_date=week_start
        )
        sunita_meals = [
            ('1', 'Breakfast', time(8, 0),   'Greek yogurt 150g + granola + mixed berries'),
            ('1', 'Lunch',     time(13, 0),  'Quinoa salad + grilled paneer 100g + lemon dressing'),
            ('1', 'Dinner',    time(20, 0),  '2 chapati + palak paneer + dal'),
            ('2', 'Breakfast', time(8, 0),   'Moong dal chilla x3 + mint chutney'),
            ('2', 'Lunch',     time(13, 0),  'Brown rice + sambar + sabzi'),
            ('2', 'Dinner',    time(20, 0),  'Chicken tikka (no gravy) 150g + salad + 1 chapati'),
            ('3', 'Breakfast', time(8, 0),   'Protein shake + 2 whole wheat toast + peanut butter'),
            ('3', 'Lunch',     time(13, 30), 'Grilled fish 130g + brown rice + sabzi'),
            ('3', 'Dinner',    time(20, 30), 'Soup + chapati + sabzi'),
        ]
        for day, meal_type, time_slot, description in sunita_meals:
            OnlineDietMeal.objects.create(
                plan=sunita_dp, day_of_week=day,
                meal_type=meal_type, time_slot=time_slot,
                description=description
            )

        self.stdout.write('  ✓ Online Workout & Diet Plans')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_progress(self):
        from accounts.models import User
        from fitness.models import UserProgress

        arjun = User.objects.get(username='arjun_online')
        entries = [
            (date.today() - timedelta(days=21), 78.5, 18.2, 38.0, 'Starting stats. Feeling motivated!'),
            (date.today() - timedelta(days=14), 77.1, 17.8, 38.5, 'Lost 1.4kg – diet going well.'),
            (date.today() - timedelta(days=7),  76.0, 17.1, 39.0, 'Good progress. Energy levels up.'),
            (date.today(),                       75.2, 16.5, 39.4, 'On track! Visible muscle definition.'),
        ]
        for d, weight, bf, mm, notes in entries:
            UserProgress.objects.create(
                member=arjun, date=d,
                weight=decimal.Decimal(str(weight)),
                body_fat_percentage=decimal.Decimal(str(bf)),
                muscle_mass_kg=decimal.Decimal(str(mm)),
                notes=notes
            )
        self.stdout.write('  ✓ Progress Records')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_orders(self):
        from accounts.models import User
        from shop.models import Product, Order, OrderItem

        arjun = User.objects.get(username='arjun_online')
        whey  = Product.objects.get(name='Whey Protein 1kg')
        creat = Product.objects.get(name='Creatine Monohydrate')
        gloves = Product.objects.get(name='Gym Gloves')
        shaker = Product.objects.get(name='Shaker Bottle 700ml')

        # Order 1 – Delivered
        o1 = Order.objects.create(
            member=arjun, total_amount=decimal.Decimal('2298'), status='delivered'
        )
        OrderItem.objects.create(order=o1, product=whey,   quantity=1, price_at_purchase=whey.price)
        OrderItem.objects.create(order=o1, product=creat,  quantity=1, price_at_purchase=creat.price)

        # Order 2 – Pending
        o2 = Order.objects.create(
            member=arjun, total_amount=decimal.Decimal('548'), status='pending'
        )
        OrderItem.objects.create(order=o2, product=gloves, quantity=1, price_at_purchase=gloves.price)
        OrderItem.objects.create(order=o2, product=shaker, quantity=1, price_at_purchase=shaker.price)

        self.stdout.write('  ✓ Orders')

    # ───────────────────────────────────────────────────────────────────────────
    def _seed_contact_messages(self):
        from core.models import ContactMessage

        messages = [
            ('Sanjay Verma',  'sanjay@gmail.com',  'I am interested in joining the gym. Can you share the membership details and fees?', False),
            ('Meena Iyer',    'meena@yahoo.com',   'Would like to know more about personal training packages. Is there a trial session?', False),
            ('Rahul Gupta',   'rahul@hotmail.com', 'I had enquired about the Gold plan last week but did not get a callback. Please respond.', False),
            ('Lakshmi Devi',  'lakshmi@gmail.com', 'What are your gym timings on weekends? Can I visit for a trial?', True),
            ('Kiran Patil',   'kiran@email.com',   'Please send me the diet plan options for weight loss. I am 30 years old, 85kg.', False),
        ]
        for name, email, message, resolved in messages:
            ContactMessage.objects.create(
                name=name, email=email, message=message, is_resolved=resolved
            )
        self.stdout.write('  ✓ Contact Messages')
