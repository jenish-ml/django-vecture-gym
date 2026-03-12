from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProgress

@login_required
def update_progress(request):
    if request.user.role != 'member' or request.user.member_type != 'online':
        messages.error(request, 'Only online members can update progress.')
        return redirect('dashboard:member_dashboard')
        
    if request.method == 'POST':
        weight = request.POST.get('weight')
        body_fat = request.POST.get('body_fat')
        muscle_mass = request.POST.get('muscle_mass')
        notes = request.POST.get('notes')
        
        if weight:
            progress = UserProgress(member=request.user, weight=weight, notes=notes)
            if body_fat:
                progress.body_fat_percentage = body_fat
            if muscle_mass:
                progress.muscle_mass_kg = muscle_mass
            progress.save()
            messages.success(request, 'Progress updated successfully!')
            return redirect('dashboard:member_dashboard')
        else:
            messages.error(request, 'Please provide your current weight.')
            
    return render(request, 'fitness/update_progress.html')
