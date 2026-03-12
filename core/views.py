from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from fitness.models import MembershipPlan, NutritionPlan
from shop.models import Product, Category
from accounts.models import User
from .models import ContactMessage

def home(request):
    membership_plans = MembershipPlan.objects.all()
    nutrition_plans = NutritionPlan.objects.all()
    # Using static images for carousel, videos, and champions via template
    context = {
        'membership_plans': membership_plans,
        'nutrition_plans': nutrition_plans,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def products_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    cat_id = request.GET.get('category')
    if cat_id:
        products = products.filter(category_id=cat_id)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'core/products_list.html', context)

def trainers_list(request):
    trainers = User.objects.filter(role='trainer', is_active=True)
    return render(request, 'core/trainers_list.html', {'trainers': trainers})

def trainer_detail(request, pk):
    trainer = get_object_or_404(User, pk=pk, role='trainer')
    return render(request, 'core/trainer_detail.html', {'trainer': trainer})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('core:contact')
    return render(request, 'core/contact.html')
