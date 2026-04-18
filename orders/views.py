from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import MenuItem, Category, Location, Order, OrderItem

def location_select(request):
    locations = Location.objects.all()
    if request.method == 'POST':
        location_id = request.POST.get('location_id')
        request.session['location_id'] = location_id
        return redirect('home')
    return render(request, 'orders/location.html', {'locations': locations})

def home(request):
    if not request.session.get('location_id'):
        return redirect('location_select')
    categories = Category.objects.all().order_by('order')
    items = MenuItem.objects.filter(is_available=True).select_related('category')
    return render(request, 'orders/home.html', {'categories': categories, 'items': items})

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('home')
    return render(request, 'orders/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid email or password.')
    return render(request, 'orders/login.html')

def logout_view(request):
    logout(request)
    return redirect('location_select')

def view_cart(request):
    cart = request.session.get('cart', [])
    items = []
    total = 0
    for entry in cart:
        item = MenuItem.objects.get(id=entry['id'])
        price = item.discounted_price()
        subtotal = price * entry['quantity']
        total += subtotal
        items.append({'item': item, 'quantity': entry['quantity'], 'subtotal': subtotal})
    return render(request, 'orders/cart.html', {'items': items, 'total': total})

def add_to_cart(request, item_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        for entry in cart:
            if entry['id'] == item_id:
                entry['quantity'] += 1
                request.session['cart'] = cart
                return JsonResponse({'status': 'updated'})
        cart.append({'id': item_id, 'quantity': 1})
        request.session['cart'] = cart
    return JsonResponse({'status': 'added'})

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    cart = [e for e in cart if e['id'] != item_id]
    request.session['cart'] = cart
    return redirect('view_cart')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('view_cart')
    items = []
    total = 0
    for entry in cart:
        item = MenuItem.objects.get(id=entry['id'])
        price = item.discounted_price()
        subtotal = price * entry['quantity']
        total += subtotal
        items.append({'item': item, 'quantity': entry['quantity'], 'subtotal': subtotal})
    if request.method == 'POST':
        location_id = request.session.get('location_id')
        location = Location.objects.get(id=location_id) if location_id else None
        order = Order.objects.create(user=request.user, total=total, location=location)
        for entry in items:
            OrderItem.objects.create(
                order=order,
                item=entry['item'],
                quantity=entry['quantity'],
                price=entry['item'].discounted_price()
            )
        request.session['cart'] = []
        messages.success(request, 'Order placed successfully!')
        return redirect('order_history')
    return render(request, 'orders/checkout.html', {'items': items, 'total': total})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

def check_email(request):
    email = request.GET.get('email', '')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})
def item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    return JsonResponse({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': float(item.price),
        'discounted_price': float(item.discounted_price()),
        'discount_percent': item.discount_percent,
        'allergens': [a.name for a in item.allergens.all()],
    })

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/profile.html', {'orders': orders})