from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.forms import inlineformset_factory
from datetime import date

from accounts.models import User, UserProfile
from fitness.models import GymGoal, MembershipPlan, NutritionPlan, WorkoutPlan, DietPlan, UserProgress, FeeTracking, OnlineWorkoutPlan, OnlineWorkoutSession, OnlineDietPlan, OnlineDietMeal
from shop.models import Product, Category, Order
from core.models import ContactMessage
from .forms import AdminUserForm, AdminTrainerForm, ProductForm, CategoryForm, MembershipPlanForm, GymGoalForm, NutritionPlanForm, FeeTrackingForm, WorkoutPlanForm, DietPlanForm, OnlineWorkoutPlanForm, OnlineWorkoutSessionForm, OnlineDietPlanForm, OnlineDietMealForm, UserUpdateForm, UserProfileUpdateForm

@login_required
def dashboard_home(request):
    if request.user.is_superuser or request.user.role == 'admin':
        return redirect('dashboard:admin_dashboard')
    elif request.user.role == 'trainer':
        return redirect('dashboard:trainer_dashboard')
    elif request.user.role == 'member':
        return redirect('dashboard:member_dashboard')
    else:
        return redirect('core:home')

@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    
    context = {
        'total_users': User.objects.count(),
        'total_trainers': User.objects.filter(role='trainer').count(),
        'total_members': User.objects.filter(role='member').count(),
        'recent_orders': Order.objects.order_by('-date_ordered')[:5],
    }
    return render(request, 'dashboard/admin/home.html', context)

@login_required
def trainer_dashboard(request):
    if request.user.role != 'trainer':
        return redirect('core:home')
    
    assigned_members = User.objects.filter(profile__trainer=request.user)
    context = {
        'assigned_members': assigned_members,
        'member_count': assigned_members.count(),
    }
    return render(request, 'dashboard/trainer/home.html', context)

# --- ADMIN VIEWS ---
@login_required
def admin_users(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    
    query = request.GET.get('q', '')
    member_type_filter = request.GET.get('member_type', '')
    
    users = User.objects.filter(role='member').order_by('-date_joined')
    
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        
    if member_type_filter:
        users = users.filter(member_type=member_type_filter)
        
    return render(request, 'dashboard/admin/users/list.html', {
        'users': users,
        'search_query': query,
        'member_type': member_type_filter
    })

@login_required
def admin_users_add(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'User added successfully.')
            return redirect('dashboard:admin_users')
    else:
        form = AdminUserForm()
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Add User', 'cancel_url': '/dashboard/admin/users/'})

@login_required
def admin_users_edit(request, user_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    user = get_object_or_404(User, id=user_id, role='member')
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('dashboard:admin_users')
    else:
        form = AdminUserForm(instance=user)
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': f'Edit {user.username}', 'cancel_url': '/dashboard/admin/users/'})

@login_required
def admin_users_delete(request, user_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    user = get_object_or_404(User, id=user_id, role='member')
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('dashboard:admin_users')

@login_required
def admin_trainers(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    
    query = request.GET.get('q', '')
    trainers = User.objects.filter(role='trainer').order_by('-date_joined')
    
    if query:
        trainers = trainers.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        
    return render(request, 'dashboard/admin/trainers/list.html', {
        'trainers': trainers,
        'search_query': query
    })

@login_required
def admin_trainers_add(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    if request.method == 'POST':
        form = AdminTrainerForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            image = form.cleaned_data.get('image')
            UserProfile.objects.create(user=user, image=image)
            messages.success(request, 'Trainer added successfully.')
            return redirect('dashboard:admin_trainers')
    else:
        form = AdminTrainerForm()
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Add Trainer', 'cancel_url': '/dashboard/admin/trainers/'})

@login_required
def admin_trainers_edit(request, user_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    trainer = get_object_or_404(User, id=user_id, role='trainer')
    if request.method == 'POST':
        form = AdminTrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            image = form.cleaned_data.get('image')
            if hasattr(trainer, 'profile'):
                if image:
                    trainer.profile.image = image
                trainer.profile.save()
            else:
                UserProfile.objects.create(user=trainer, image=image)
            messages.success(request, 'Trainer updated successfully.')
            return redirect('dashboard:admin_trainers')
    else:
        initial = {}
        if hasattr(trainer, 'profile') and trainer.profile.image:
            initial['image'] = trainer.profile.image
        form = AdminTrainerForm(instance=trainer, initial=initial)
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': f'Edit {trainer.username}', 'cancel_url': '/dashboard/admin/trainers/'})

@login_required
def admin_trainers_delete(request, user_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    trainer = get_object_or_404(User, id=user_id, role='trainer')
    trainer.delete()
    messages.success(request, 'Trainer deleted successfully.')
    return redirect('dashboard:admin_trainers')

@login_required
def admin_products(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()
    return render(request, 'dashboard/admin/products/list.html', {'products': products, 'categories': categories})

@login_required
def admin_products_add(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('dashboard:admin_products')
    else:
        form = ProductForm()
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Add Product', 'cancel_url': '/dashboard/admin/products/'})

@login_required
def admin_category_add(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('dashboard:admin_products')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Add Product Category', 'cancel_url': '/dashboard/admin/products/'})

@login_required
def admin_products_edit(request, product_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('dashboard:admin_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': f'Edit {product.name}', 'cancel_url': '/dashboard/admin/products/'})

@login_required
def admin_products_delete(request, product_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
    return redirect('dashboard:admin_products')

@login_required
def admin_plans(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    memberships = MembershipPlan.objects.all()
    nutrition_plans = NutritionPlan.objects.all()
    goals = GymGoal.objects.all()
    return render(request, 'dashboard/admin/plans/list.html', {
        'memberships': memberships,
        'nutritions': nutrition_plans,
        'goals': goals
    })

# --- Membership Plans CRUD ---
@login_required
def admin_membership_add(request):
    if not (request.user.is_superuser or request.user.role == 'admin'): return redirect('core:home')
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership Plan added.')
            return redirect('dashboard:admin_plans')
    else: form = MembershipPlanForm()
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Add Membership Plan', 'cancel_url': '/dashboard/admin/plans/'})

@login_required
def admin_membership_edit(request, plan_id):
    if not (request.user.is_superuser or request.user.role == 'admin'): return redirect('core:home')
    plan = get_object_or_404(MembershipPlan, id=plan_id)
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership Plan updated.')
            return redirect('dashboard:admin_plans')
    else: form = MembershipPlanForm(instance=plan)
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': f'Edit {plan.name}', 'cancel_url': '/dashboard/admin/plans/'})

@login_required
def admin_membership_delete(request, plan_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    plan = get_object_or_404(MembershipPlan, id=plan_id)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Membership plan deleted successfully.')
    return redirect('dashboard:admin_plans')

# --- Nutrition Plans CRUD ---
@login_required
def admin_nutrition_add(request):
    if not (request.user.is_superuser or request.user.role == 'admin'): return redirect('core:home')
    if request.method == 'POST':
        form = NutritionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nutrition Plan added.')
            return redirect('dashboard:admin_plans')
    else: form = NutritionPlanForm()
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Add Nutrition Plan', 'cancel_url': '/dashboard/admin/plans/'})

@login_required
def admin_nutrition_edit(request, plan_id):
    if not (request.user.is_superuser or request.user.role == 'admin'): return redirect('core:home')
    plan = get_object_or_404(NutritionPlan, id=plan_id)
    if request.method == 'POST':
        form = NutritionPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nutrition Plan updated.')
            return redirect('dashboard:admin_plans')
    else: form = NutritionPlanForm(instance=plan)
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': f'Edit {plan.name}', 'cancel_url': '/dashboard/admin/plans/'})

@login_required
def admin_nutrition_delete(request, plan_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    plan = get_object_or_404(NutritionPlan, id=plan_id)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Nutrition plan deleted successfully.')
    return redirect('dashboard:admin_plans')

# --- Gym Goals CRUD ---
@login_required
def admin_goal_add(request):
    if not (request.user.is_superuser or request.user.role == 'admin'): return redirect('core:home')
    if request.method == 'POST':
        form = GymGoalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gym Goal added.')
            return redirect('dashboard:admin_plans')
    else: form = GymGoalForm()
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Add Gym Goal', 'cancel_url': '/dashboard/admin/plans/'})

@login_required
def admin_goal_edit(request, goal_id):
    if not (request.user.is_superuser or request.user.role == 'admin'): return redirect('core:home')
    goal = get_object_or_404(GymGoal, id=goal_id)
    if request.method == 'POST':
        form = GymGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gym Goal updated.')
            return redirect('dashboard:admin_plans')
    else: form = GymGoalForm(instance=goal)
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': f'Edit {goal.name}', 'cancel_url': '/dashboard/admin/plans/'})

@login_required
def admin_goal_delete(request, goal_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    goal = get_object_or_404(GymGoal, id=goal_id)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully.')
    return redirect('dashboard:admin_plans')

@login_required
def admin_payments(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    
    # E-commerce orders
    orders = Order.objects.all().order_by('-date_ordered')
    
    # Membership Fees
    fees = FeeTracking.objects.all().order_by('-due_date')
    
    return render(request, 'dashboard/admin/payments/list.html', {
        'orders': orders,
        'fees': fees
    })

@login_required
def admin_fee_add(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    if request.method == 'POST':
        form = FeeTrackingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record added successfully.')
            return redirect('dashboard:admin_payments')
    else:
        form = FeeTrackingForm()
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Add Fee Record', 'cancel_url': '/dashboard/admin/payments/'})

@login_required
def admin_fee_edit(request, fee_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    fee = get_object_or_404(FeeTracking, id=fee_id)
    if request.method == 'POST':
        form = FeeTrackingForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record updated successfully.')
            return redirect('dashboard:admin_payments')
    else:
        form = FeeTrackingForm(instance=fee)
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Edit Fee Record', 'cancel_url': '/dashboard/admin/payments/'})

@login_required
def admin_payment_detail(request, order_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}.')
        return redirect('dashboard:admin_payment_detail', order_id=order.id)

    return render(request, 'dashboard/admin/payments/detail.html', {'order': order})

@login_required
def admin_messages(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    messages_list = ContactMessage.objects.all().order_by('-date_sent')
    return render(request, 'dashboard/admin/messages/list.html', {'contact_messages': messages_list})

@login_required
def admin_message_detail(request, msg_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    msg = get_object_or_404(ContactMessage, id=msg_id)
    
    if request.method == 'POST':
        reply_content = request.POST.get('reply_message')
        if reply_content:
            try:
                send_mail(
                    subject=f"Re: Your message to Vecture Gym",
                    message=reply_content,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'admin@vecture.com',
                    recipient_list=[msg.email],
                    fail_silently=False,
                )
                msg.is_resolved = True
                msg.save()
                messages.success(request, f"Reply sent to {msg.email} and message marked as resolved!")
            except Exception as e:
                messages.error(request, f"Failed to send email: {str(e)}")
        else:
            messages.error(request, "Reply message cannot be empty.")

    return redirect('dashboard:admin_messages')

@login_required
def admin_resolve_message(request, msg_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    msg = get_object_or_404(ContactMessage, id=msg_id)
    msg.is_resolved = True
    msg.save()
    messages.success(request, 'Message marked as resolved.')
    return redirect('dashboard:admin_messages')

@login_required
def admin_message_delete(request, msg_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    if request.method == 'POST':
        msg = get_object_or_404(ContactMessage, id=msg_id)
        msg.delete()
        messages.success(request, 'Message deleted successfully.')
    return redirect('dashboard:admin_messages')

@login_required
def admin_profile(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('core:home')
    
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:admin_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SetPasswordForm(request.user)
        
    return render(request, 'dashboard/admin/profile/view.html', {'form': form})


# --- TRAINER VIEWS ---
@login_required
def trainer_view_users(request):
    if request.user.role != 'trainer':
        return redirect('core:home')
    assigned_members = User.objects.filter(profile__trainer=request.user)
    return render(request, 'dashboard/trainer/home.html', {'assigned_members': assigned_members})

@login_required
def trainer_assign_workout(request):
    if request.user.role != 'trainer': return redirect('core:home')
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST, trainer=request.user)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.trainer = request.user
            plan.save()
            messages.success(request, 'Workout plan assigned successfully.')
            return redirect('dashboard:trainer_dashboard')
    else:
        form = WorkoutPlanForm(trainer=request.user)
    return render(request, 'dashboard/trainer/assign_workout.html', {'form': form, 'title': 'Assign Workout Plan (Offline)', 'cancel_url': '/dashboard/trainer/'})

@login_required
def trainer_assign_online_workout(request):
    if request.user.role != 'trainer': return redirect('core:home')
    
    SessionFormSet = inlineformset_factory(OnlineWorkoutPlan, OnlineWorkoutSession, form=OnlineWorkoutSessionForm, extra=1, can_delete=False)
    
    if request.method == 'POST':
        form = OnlineWorkoutPlanForm(request.POST, trainer=request.user)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.trainer = request.user
            formset = SessionFormSet(request.POST, request.FILES, instance=plan)
            if formset.is_valid():
                plan.save()
                formset.save()
                messages.success(request, 'Online Workout plan assigned successfully.')
                return redirect('dashboard:trainer_dashboard')
        else:
            formset = SessionFormSet(request.POST, request.FILES)
    else:
        form = OnlineWorkoutPlanForm(trainer=request.user)
        formset = SessionFormSet()
        
    return render(request, 'dashboard/trainer/assign_online_workout.html', {'form': form, 'formset': formset, 'title': 'Assign Online Workout Plan', 'cancel_url': '/dashboard/trainer/'})

@login_required
def trainer_assign_diet(request):
    if request.user.role != 'trainer': return redirect('core:home')
    if request.method == 'POST':
        form = DietPlanForm(request.POST, trainer=request.user)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.trainer = request.user
            plan.save()
            messages.success(request, 'Diet plan assigned successfully.')
            return redirect('dashboard:trainer_dashboard')
    else:
        form = DietPlanForm(trainer=request.user)
    return render(request, 'dashboard/admin/generic/form.html', {'form': form, 'title': 'Assign Diet Plan (Offline)', 'cancel_url': '/dashboard/trainer/'})

@login_required
def trainer_assign_online_diet(request):
    if request.user.role != 'trainer': return redirect('core:home')
    
    MealFormSet = inlineformset_factory(OnlineDietPlan, OnlineDietMeal, form=OnlineDietMealForm, extra=1, can_delete=False)
    
    if request.method == 'POST':
        form = OnlineDietPlanForm(request.POST, trainer=request.user)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.trainer = request.user
            formset = MealFormSet(request.POST, instance=plan)
            if formset.is_valid():
                plan.save()
                formset.save()
                messages.success(request, 'Online Diet plan assigned successfully.')
                return redirect('dashboard:trainer_dashboard')
        else:
            formset = MealFormSet(request.POST)
    else:
        form = OnlineDietPlanForm(trainer=request.user)
        formset = MealFormSet()
        
    return render(request, 'dashboard/trainer/assign_online_diet.html', {'form': form, 'formset': formset, 'title': 'Assign Online Diet Plan', 'cancel_url': '/dashboard/trainer/'})

@login_required
def trainer_profile(request):
    if request.user.role != 'trainer': return redirect('core:home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile details were successfully updated!')
                return redirect('dashboard:trainer_profile')
            else:
                messages.error(request, 'Please correct the errors below.')
                pass_form = SetPasswordForm(request.user)
        elif action == 'update_password':
            pass_form = SetPasswordForm(request.user, request.POST)
            user_form = UserUpdateForm(instance=request.user)
            profile_form = UserProfileUpdateForm(instance=request.user.profile)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('dashboard:trainer_profile')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        pass_form = SetPasswordForm(request.user)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)
        
    return render(request, 'dashboard/trainer/profile/view.html', {
        'pass_form': pass_form,
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def view_member_progress(request, member_id):
    if request.user.role != 'trainer':
        return redirect('core:home')
        
    member = get_object_or_404(User, id=member_id, profile__trainer=request.user)
    logs = UserProgress.objects.filter(member=member).order_by('-date')
    reversed_logs = reversed(logs) # Chronological for Chart
    
    latest_online_workout = OnlineWorkoutPlan.objects.filter(member=member).order_by('-week_start_date').first()
    latest_online_diet = OnlineDietPlan.objects.filter(member=member).order_by('-week_start_date').first()
    
    context = {
        'member': member,
        'logs': logs,
        'reversed_logs': reversed_logs,
        'latest_online_workout': latest_online_workout,
        'latest_online_diet': latest_online_diet
    }
    return render(request, 'dashboard/trainer/view_progress.html', context)
    
@login_required
def member_dashboard(request):
    if request.user.role != 'member':
        return redirect('core:home')
    
    profile = request.user.profile
    recent_progress = UserProgress.objects.filter(member=request.user).order_by('-date')[:5]
    recent_orders = Order.objects.filter(member=request.user).order_by('-date_ordered')[:5]
    user_fees = FeeTracking.objects.filter(member=request.user).order_by('due_date')
    today = date.today()
    for fee in user_fees:
        if fee.due_date and fee.status != 'Paid':
            delta = (fee.due_date - today).days
            fee.remaining_days = delta if delta > 0 else 0
        else:
            fee.remaining_days = None
            
    # Advanced Online Plans
    latest_online_workout = OnlineWorkoutPlan.objects.filter(member=request.user).order_by('-week_start_date').first()
    latest_online_diet = OnlineDietPlan.objects.filter(member=request.user).order_by('-week_start_date').first()
    
    context = {
        'profile': profile,
        'recent_progress': recent_progress,
        'recent_orders': recent_orders,
        'user_fees': user_fees,
        'latest_online_workout': latest_online_workout,
        'latest_online_diet': latest_online_diet,
    }
    return render(request, 'dashboard/member/home.html', context)

@login_required
def member_profile(request):
    if request.user.role != 'member': return redirect('core:home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile details were successfully updated!')
                return redirect('dashboard:member_profile')
            else:
                messages.error(request, 'Please correct the errors below.')
                pass_form = SetPasswordForm(request.user)
        elif action == 'update_password':
            pass_form = SetPasswordForm(request.user, request.POST)
            user_form = UserUpdateForm(instance=request.user)
            profile_form = UserProfileUpdateForm(instance=request.user.profile)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('dashboard:member_profile')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        pass_form = SetPasswordForm(request.user)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)
        
    return render(request, 'dashboard/member/profile/view.html', {
        'pass_form': pass_form,
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def member_nutrition(request):
    if request.user.role != 'member':
        return redirect('core:home')
    profile = request.user.profile
    return render(request, 'dashboard/member/nutrition.html', {'profile': profile})


@login_required
def member_goals(request):
    if request.user.role != 'member':
        return redirect('core:home')
    profile = request.user.profile
    return render(request, 'dashboard/member/goals.html', {'profile': profile})

@login_required
def member_products(request):
    if request.user.role != 'member':
        return redirect('core:home')
        
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if category_id:
        products = products.filter(category_id=category_id)
        
    context = {
        'products': products,
        'categories': categories,
        'search_query': query,
        'current_category': int(category_id) if category_id else ''
    }
    return render(request, 'dashboard/member/products.html', context)


@login_required
def member_fee_checkout(request, fee_id):
    """Show the fee payment page with card / UPI options."""
    if request.user.role != 'member':
        return redirect('core:home')
    fee = get_object_or_404(FeeTracking, id=fee_id, member=request.user)
    if fee.status == 'Paid':
        messages.info(request, 'This fee has already been paid.')
        return redirect('dashboard:member_dashboard')
    return render(request, 'dashboard/member/fee_pay.html', {'fee': fee})


@login_required
def member_pay_fee(request, fee_id):
    """Process fee payment and mark as Paid."""
    if request.user.role != 'member':
        return redirect('core:home')

    fee = get_object_or_404(FeeTracking, id=fee_id, member=request.user)

    if request.method == 'POST':
        if fee.status != 'Paid':
            payment_method = request.POST.get('payment_method', 'card')
            fee.status = 'Paid'
            fee.amount_paid = fee.amount_due
            fee.save()
            method_label = 'Card' if payment_method == 'card' else 'UPI/Online'
            messages.success(request, f'Payment of ₹{fee.amount_due} via {method_label} was successful! ✓')
        else:
            messages.info(request, 'This fee has already been paid.')
    return redirect('dashboard:member_dashboard')
