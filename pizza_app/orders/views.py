from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Pizza, Drink, Order, OrderItem, Coupon, Location
from .forms import PizzaCartForm, DrinkCartForm, CheckoutForm


def menu(request):
    pizzas = Pizza.objects.all().prefetch_related('available_toppings')
    drinks = Drink.objects.all()

    pizza_forms = {}
    for pizza in pizzas:
        pizza_forms[pizza.id] = PizzaCartForm(prefix=f"pizza_{pizza.id}", pizza=pizza)

    drink_forms = {}
    for drink in drinks:
        drink_forms[drink.id] = DrinkCartForm(prefix=f"drink_{drink.id}")

    return render(request, 'orders/menu.html', {
        'pizzas': pizzas,
        'drinks': drinks,
        'pizza_forms': pizza_forms,
        'drink_forms': drink_forms,
    })


def register(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        if not username or not password:
            error = 'Username and password are required.'
        elif User.objects.filter(username=username).exists():
            error = 'That username is already taken. Please choose another.'
        else:
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')

    return render(request, 'orders/register.html', {'error': error})


@login_required
def add_pizza_to_cart(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    form = PizzaCartForm(request.POST, prefix=f"pizza_{pizza.id}", pizza=pizza)

    if form.is_valid():
        size = form.cleaned_data['size']
        quantity = form.cleaned_data['quantity']
        selected_toppings = form.cleaned_data.get('toppings', [])

        if size == 'S':
            base_price = float(pizza.price_small)
        elif size == 'M':
            base_price = float(pizza.price_medium)
        else:
            base_price = float(pizza.price_large)

        topping_extra = 0
        topping_names = []
        for topping in selected_toppings:
            topping_names.append(topping.name)
            if size == 'S':
                topping_extra += float(topping.price_small)
            elif size == 'M':
                topping_extra += float(topping.price_medium)
            else:
                topping_extra += float(topping.price_large)

        unit_price = round(base_price + topping_extra, 2)
        cart = request.session.get('cart', [])
        cart.append({
            'type': 'pizza',
            'id': pizza.id,
            'name': pizza.name,
            'size': size,
            'quantity': quantity,
            'price': unit_price,
            'subtotal': round(unit_price * quantity, 2),
            'toppings': topping_names,
            'emoji': pizza.emoji,
        })
        request.session['cart'] = cart
        messages.success(request, f'{pizza.name} added to cart!')

    return redirect('menu')


@login_required
def add_drink_to_cart(request, drink_id):
    drink = get_object_or_404(Drink, id=drink_id)
    form = DrinkCartForm(request.POST, prefix=f"drink_{drink.id}")

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        price = float(drink.price)
        cart = request.session.get('cart', [])
        cart.append({
            'type': 'drink',
            'id': drink.id,
            'name': drink.name,
            'quantity': quantity,
            'price': price,
            'subtotal': round(price * quantity, 2),
            'toppings': [],
            'emoji': drink.emoji,
        })
        request.session['cart'] = cart
        messages.success(request, f'{drink.name} added to cart!')

    return redirect('menu')


@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    subtotal = round(sum(item['subtotal'] for item in cart), 2)
    coupon = request.session.get('coupon')
    discount = 0
    if coupon:
        discount = round(subtotal * coupon['discount'] / 100, 2)
    total = round(subtotal - discount, 2)

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'coupon': coupon,
    })


@login_required
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip().upper()
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            request.session['coupon'] = {'code': coupon.code, 'discount': coupon.discount_percent}
            messages.success(request, f'Coupon "{coupon.code}" applied! {coupon.discount_percent}% discount.')
        except Coupon.DoesNotExist:
            request.session['coupon'] = None
            messages.error(request, 'That coupon code is invalid or expired.')
    return redirect('view_cart')


@login_required
def remove_coupon(request):
    request.session['coupon'] = None
    messages.info(request, 'Coupon removed.')
    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_index):
    cart = request.session.get('cart', [])
    if 0 <= item_index < len(cart):
        removed = cart.pop(item_index)
        request.session['cart'] = cart
        messages.info(request, f'{removed["name"]} removed from cart.')
    return redirect('view_cart')


@login_required
def clear_cart(request):
    request.session['cart'] = []
    request.session['coupon'] = None
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('view_cart')

    subtotal = round(sum(item['subtotal'] for item in cart), 2)
    coupon = request.session.get('coupon')
    discount = 0
    coupon_code = ''
    if coupon:
        discount = round(subtotal * coupon['discount'] / 100, 2)
        coupon_code = coupon['code']
    total = round(subtotal - discount, 2)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            delivery_address = form.cleaned_data['delivery_address']
            order = Order.objects.create(
                user=request.user,
                total_price=total,
                status='P',
                delivery_address=delivery_address,
                coupon_code=coupon_code,
                discount_amount=discount,
            )

            for item in cart:
                if item['type'] == 'pizza':
                    pizza = get_object_or_404(Pizza, id=item['id'])
                    OrderItem.objects.create(
                        order=order,
                        pizza=pizza,
                        drink=None,
                        quantity=item['quantity'],
                        size=item['size'],
                    )
                elif item['type'] == 'drink':
                    drink = get_object_or_404(Drink, id=item['id'])
                    OrderItem.objects.create(
                        order=order,
                        pizza=None,
                        drink=drink,
                        quantity=item['quantity'],
                        size=None,
                    )

            request.session['cart'] = []
            request.session['coupon'] = None
            messages.success(request, f'Order #{order.id} placed! We will prepare it shortly.')
            return redirect('order_history')
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'coupon': coupon,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'orders/order_history.html', {'orders': orders})


def locations(request):
    location_list = Location.objects.all()
    return render(request, 'orders/locations.html', {'locations': location_list})


@login_required
def reorder(request, order_id):
    """Copy all items from a past order back into the cart."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = request.session.get('cart', [])
    added = 0

    for item in order.orderitem_set.all():
        if item.pizza:
            size = item.size or 'M'
            if size == 'S':
                price = float(item.pizza.price_small)
            elif size == 'M':
                price = float(item.pizza.price_medium)
            else:
                price = float(item.pizza.price_large)
            cart.append({
                'type': 'pizza',
                'id': item.pizza.id,
                'name': item.pizza.name,
                'size': size,
                'quantity': item.quantity,
                'price': price,
                'subtotal': round(price * item.quantity, 2),
                'toppings': [],
                'emoji': item.pizza.emoji,
            })
            added += 1
        elif item.drink:
            price = float(item.drink.price)
            cart.append({
                'type': 'drink',
                'id': item.drink.id,
                'name': item.drink.name,
                'quantity': item.quantity,
                'price': price,
                'subtotal': round(price * item.quantity, 2),
                'toppings': [],
                'emoji': item.drink.emoji,
            })
            added += 1

    request.session['cart'] = cart
    messages.success(request, f'Order #{order.id} added to your cart ({added} item{"s" if added != 1 else ""}).')
    return redirect('view_cart')
