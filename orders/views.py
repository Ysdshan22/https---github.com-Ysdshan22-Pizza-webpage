from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Pizza, Drink, Order, OrderItem, Side, Topping
from .forms import PizzaCartForm, DrinkCartForm, CheckoutForm


def get_pizza_image(name):
    n = name.lower()

    if 'margherita' in n:
        return 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=800&q=80'
    elif 'pepperoni' in n:
        return 'https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=800&q=80'
    elif 'picante' in n or 'pikanta' in n or 'spicy' in n:
        return 'https://images.unsplash.com/photo-1548369937-47519962c11a?auto=format&fit=crop&w=800&q=80'
    elif 'beef' in n:
        return 'https://images.unsplash.com/photo-1621070766841-a7bf1ee96df0?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'chicken' in n:
        return 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=800&q=80'
    elif 'nduja' in n:
        return 'https://images.unsplash.com/photo-1594007654729-407eedc4be65?q=80&w=728&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'truffle' in n:
        return 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80'
    elif 'salami' in n:
        return 'https://images.unsplash.com/photo-1712460840521-04846c6b1c8b?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'tomat' in n or 'tomato' in n:
        return 'https://images.unsplash.com/photo-1669895616443-5d21d5acc6e0?q=80&w=1025&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'devil' in n:
        return 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80'
    else:
        return 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80'


def get_drink_image(name):
    n = name.lower()

    if 'cola' in n or 'coca' in n:
        return 'https://plus.unsplash.com/premium_photo-1725075086631-b21a5642918b?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'fanta' in n or 'orange' in n:
        return 'https://images.unsplash.com/photo-1624517452488-04869289c4ca?q=80&w=803&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'pepsi' in n:
        return 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?q=80&w=1229&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'farris' in n or 'water' in n or 'vann' in n:
        return 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?auto=format&fit=crop&w=600&q=80'
    elif 'solo' in n or 'lemon' in n:
        return 'https://images.unsplash.com/photo-1766050587712-72b737dc1d39?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'sprite' in n or 'sprit' in n:
        return 'https://images.unsplash.com/photo-1680404005217-a441afdefe83?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'red bull' in n or 'energy' in n:
        return 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?auto=format&fit=crop&w=600&q=80'
    else:
        return 'https://images.unsplash.com/photo-1543253687-c931c8e01820?auto=format&fit=crop&w=600&q=80'


def get_side_image(name, side_type):
    n = name.lower()

    # DIPS
    if 'truffle' in n:
        return 'https://images.unsplash.com/photo-1617331721523-74863928da29?q=80&w=1972&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'bbq' in n:
        return 'https://images.unsplash.com/photo-1516407019386-e27ad4597cf6?q=80&w=1209&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'spicy cheddar' in n:
        return 'https://images.unsplash.com/photo-1722239312531-486bbfd50f18?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'spicy' in n:
        return 'https://images.unsplash.com/photo-1722239312531-486bbfd50f18?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'classic' in n:
        return 'https://images.unsplash.com/photo-1628520381646-0ab983902c65?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'

    
    elif 'fish' in n:
        return 'https://images.unsplash.com/photo-1655690125465-5947c227d836?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'chicken nugget' in n:
        return 'https://images.unsplash.com/photo-1619881590738-a111d176d906?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'mozzarella' in n:
        return 'https://images.unsplash.com/photo-1548340748-6d2b7d7da280'
    elif 'chilli poppers' in n:
        return 'https://images.unsplash.com/photo-1585039261108-ec658b915e37?q=80&w=797&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'churros' in n:
        return 'https://plus.unsplash.com/premium_photo-1713687789756-b38c7870eef6?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    elif 'salat' in n or 'salad' in n:
        return 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'

    return 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38'

def menu(request):
    pizzas = Pizza.objects.all()
    drinks = Drink.objects.all()
    sides = Side.objects.filter(side_type__in=['nuggets', 'mozzarella', 'churros', 'chilli', 'salad'])
    dips = Side.objects.filter(side_type='dip')

    pizza_data = []
    for pizza in pizzas:
        pizza.fallback_image = get_pizza_image(pizza.name)
        form = PizzaCartForm(prefix=f"pizza_{pizza.id}")
        form.fields['toppings'].queryset = pizza.available_toppings.all()

        pizza_data.append({
            'pizza': pizza,
            'form': form,
        })

    drink_forms = {}
    for drink in drinks:
        drink.display_image = get_drink_image(drink.name)
        drink_forms[drink.id] = DrinkCartForm(prefix=f"drink_{drink.id}")

    for side in sides:
        side.display_image = get_side_image(side.name, side.side_type)

    for dip in dips:
        dip.display_image = get_side_image(dip.name, dip.side_type)

    return render(request, 'orders/menu.html', {
        'pizza_data': pizza_data,
        'drinks': drinks,
        'drink_forms': drink_forms,
        'sides': sides,
        'dips': dips,
        'cart_count': len(request.session.get('cart', [])),
    })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'orders/register.html')


@login_required
def add_pizza_to_cart(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)

    if request.method == 'POST':
        form = PizzaCartForm(request.POST, prefix=f"pizza_{pizza.id}")
        form.fields['toppings'].queryset = Topping.objects.all()

        if form.is_valid():
            size = form.cleaned_data['size']
            quantity = form.cleaned_data['quantity']
            toppings = form.cleaned_data['toppings']
            meal_drink = request.POST.get('meal_drink')
            meal_side = request.POST.get('meal_side')

            if size == 'S':
                base_price = float(pizza.price_small)
            elif size == 'M':
                base_price = float(pizza.price_medium)
            else:
                base_price = float(pizza.price_large)

            topping_names = []
            topping_ids = []
            toppings_total = 0

            for topping in toppings:
                topping_names.append(topping.name)
                topping_ids.append(topping.id)

                if size == 'S':
                    toppings_total += float(topping.price_small)
                elif size == 'M':
                    toppings_total += float(topping.price_medium)
                else:
                    toppings_total += float(topping.price_large)

            unit_price = base_price + toppings_total
            subtotal = unit_price * quantity

            cart = request.session.get('cart', [])
            if meal_drink and meal_side:

                drink = Drink.objects.get(id=meal_drink)
                side = Side.objects.get(id=meal_side)

                cart.append({
                    'type': 'meal_deal',

                    'id': pizza.id,
                    'name': f"{pizza.name} Meal Deal",

                    'pizza_name': pizza.name,
                    'drink_name': drink.name,
                    'side_name': side.name,

                    'image': pizza.image.url if pizza.image else get_pizza_image(pizza.name),

                    'size': size,
                    'quantity': quantity,

                    'price': unit_price + float(drink.price) + float(side.price),

                    'subtotal':
                        (unit_price + float(drink.price) + float(side.price))
                        * quantity,

                    'toppings': topping_names,
                    'topping_ids': topping_ids,
                })

            else:

                cart.append({
                    'type': 'pizza',
                    'id': pizza.id,
                    'name': pizza.name,
                    'image': pizza.image.url if pizza.image else get_pizza_image(pizza.name),
                    'size': size,
                    'quantity': quantity,
                    'price': unit_price,
                    'subtotal': subtotal,
                    'toppings': topping_names,
                    'topping_ids': topping_ids,
                })
            request.session['cart'] = cart

            messages.success(request, "Pizza added to cart successfully.")

    return redirect('menu')


@login_required
def add_drink_to_cart(request, drink_id):
    drink = get_object_or_404(Drink, id=drink_id)

    if request.method == 'POST':
        form = DrinkCartForm(request.POST, prefix=f"drink_{drink.id}")

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            price = float(drink.price)

            cart = request.session.get('cart', [])
            cart.append({
                'type': 'drink',
                'id': drink.id,
                'name': drink.name,
                'image': get_drink_image(drink.name),
                'quantity': quantity,
                'price': price,
                'subtotal': price * quantity,
            })
            request.session['cart'] = cart

            messages.success(request, "Drink added to cart successfully.")

    return redirect('menu')
@login_required
def add_side_to_cart(request, side_id):
    side = get_object_or_404(Side, id=side_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        price = float(side.price)

        cart = request.session.get('cart', [])
        cart.append({
            'type': 'side',
            'id': side.id,
            'name': side.name,
            'image': get_side_image(side.name, side.side_type),
            'quantity': quantity,
            'price': price,
            'subtotal': price * quantity,
        })
        request.session['cart'] = cart

        messages.success(request, "Item added to cart successfully.")

    return redirect('menu')


@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['subtotal'] for item in cart)

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'total': total,
    })


@login_required
def remove_from_cart(request, item_index):
    cart = request.session.get('cart', [])

    if 0 <= item_index < len(cart):
        cart.pop(item_index)
        request.session['cart'] = cart

    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


@login_required
def clear_cart(request):
    request.session['cart'] = []
    messages.success(request, "Cart cleared successfully.")
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', [])
    total = sum(item['subtotal'] for item in cart)

    if not cart:
        return redirect('view_cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            delivery_address = form.cleaned_data['delivery_address']

            order = Order.objects.create(
                user=request.user,
                total_price=total,
                status='P',
                delivery_address=delivery_address
            )

            for item in cart:
                if item['type'] == 'pizza':
                    pizza = get_object_or_404(Pizza, id=item['id'])

                    order_item = OrderItem.objects.create(
                        order=order,
                        pizza=pizza,
                        drink=None,
                        side=None,
                        quantity=item['quantity'],
                        size=item['size'],
                        dietary=''
                    )

                    if 'topping_ids' in item:
                        selected_toppings = Topping.objects.filter(id__in=item['topping_ids'])
                        order_item.toppings.set(selected_toppings)

                elif item['type'] == 'drink':
                    drink = get_object_or_404(Drink, id=item['id'])
                    OrderItem.objects.create(
                        order=order,
                        pizza=None,
                        drink=drink,
                        side=None,
                        quantity=item['quantity'],
                        size=None,
                        dietary=''
                    )

            request.session['cart'] = []
            messages.success(request, "Your order has been placed successfully.")
            return redirect('menu')
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'total': total,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')

    return render(request, 'orders/order_history.html', {
        'orders': orders
    })