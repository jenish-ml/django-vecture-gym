from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem
from fitness.models import MembershipPlan

def _member_required(request):
    """Returns True if the user is a member (online or offline)."""
    return request.user.is_authenticated and request.user.role == 'member'

@login_required
def add_to_cart(request, product_id):
    if not _member_required(request):
        messages.error(request, 'Only members can shop products.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(member=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{product.name} added to your cart.')
    return redirect(request.META.get('HTTP_REFERER', '/dashboard/member/products/'))

@login_required
def view_cart(request):
    if not _member_required(request):
        return redirect('dashboard:member_dashboard')

    cart, created = Cart.objects.get_or_create(member=request.user)
    items = cart.items.all().order_by('id')
    total = sum([item.product.price * item.quantity for item in items])

    return render(request, 'shop/cart.html', {'items': items, 'total': total})

@login_required
def update_cart(request, item_id):
    if not _member_required(request):
        return redirect('dashboard:member_dashboard')

    cart_item = get_object_or_404(CartItem, id=item_id, cart__member=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Increased quantity for {cart_item.product.name}.')
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, f'Decreased quantity for {cart_item.product.name}.')
            else:
                cart_item.delete()
                messages.success(request, f'{cart_item.product.name} removed from your cart.')

    next_url = request.POST.get('next', 'shop:view_cart')
    return redirect(next_url)

@login_required
def remove_from_cart(request, item_id):
    if not _member_required(request):
        return redirect('dashboard:member_dashboard')

    cart_item = get_object_or_404(CartItem, id=item_id, cart__member=request.user)

    if request.method == 'POST':
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'{product_name} removed from your cart.')

    next_url = request.POST.get('next', 'shop:view_cart')
    return redirect(next_url)

@login_required
def checkout(request):
    if not _member_required(request):
        return redirect('dashboard:member_dashboard')

    cart, created = Cart.objects.get_or_create(member=request.user)
    items = cart.items.all()

    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('shop:view_cart')

    if request.method == 'POST':
        total = sum([item.product.price * item.quantity for item in items])
        order = Order.objects.create(member=request.user, total_amount=total, status='paid')
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
        items.delete()
        messages.success(request, 'Order placed successfully! 🎉')
        return redirect('dashboard:member_dashboard')

    total = sum([item.product.price * item.quantity for item in items])
    return render(request, 'shop/checkout.html', {'items': items, 'total': total})
