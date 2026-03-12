from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import User, UserProfile

def register_view(request):
    # Pre-select trainer or plan based on URL params from public pages
    initial_data = {}
    if 'trainer' in request.GET:
        initial_data['trainer'] = request.GET['trainer']
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'member'
            user.member_type = form.cleaned_data.get('member_type')
            user.save()

            # Create UserProfile based on member role
            profile_data = {'user': user}
            
            profile_data['fitness_goal'] = form.cleaned_data.get('fitness_goal')
            profile_data['trainer'] = form.cleaned_data.get('trainer')
            profile_data['membership_plan'] = form.cleaned_data.get('membership_plan')
            
            member_type = form.cleaned_data.get('member_type')
            if member_type == 'offline':
                profile_data['nutrition_plan'] = form.cleaned_data.get('nutrition_plan')
                
            UserProfile.objects.create(**profile_data)
            
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('accounts:login')
    else:
        form = RegistrationForm(initial=initial_data)

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:dashboard_home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('core:home')
