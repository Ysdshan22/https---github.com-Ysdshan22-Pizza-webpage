from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pizza, Drink, Order, OrderItem, Side
from .forms import PizzaCartForm, DrinkCartForm, CheckoutForm


def get_pizza_image(name):
    n = name.lower()
    if 'margherita' in n: return 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&q=80'
    if 'pepperoni' in n: return 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&q=80'
    if 'picante' in n or 'pikanta' in n: return 'https://images.unsplash.com/photo-1548369937-47519962c11a?w=400&q=80'
    if 'beef' in n: return 'https://unsplash.com/photos/pizza-on-brown-wooden-tray-oYkC51pOQBk'
    if 'chicken' in n: return 'https://unsplash.com/photos/a-pizza-sitting-on-top-of-a-white-plate-DEzv3gH5rIg'
    if 'nduja' in n: return 'https://unsplash.com/photos/round-cooked-pizza-x00CzBt4Dfk'
    if 'truffle salami' in n or 'salami' in n: return 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&q=80'
    if 'tomat' in n: return 'https://unsplash.com/photos/a-pizza-with-tomatoes-and-basil-otZSAyb65_o'
    if 'devil' in n: return 'https://images.unsplash.com/photo-1481070414801-51fd732d7184?w=400&q=80'
    return 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80'


def get_drink_image(name):
    n = name.lower()
    if 'cola' in n or 'coca' in n: return 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=300&q=80'
    if 'fanta' in n: return 'https://unsplash.com/photos/fanta-orange-can-on-brown-wooden-table-aKYu-H5pHJY'
    if 'pepsi' in n: return 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300&q=80'
    if 'farris' in n or 'water' in n or 'vann' in n: return 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300&q=80'
    if 'solo' in n: return 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300&q=80'
    if 'sprite' in n or 'sprit' in n: return 'https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=300&q=80'
    if 'red bull' in n or 'energy' in n: return 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300&q=80'
    return 'https://images.unsplash.com/photo-1581636625402-29b2a704ef13?w=300&q=80'


def get_side_image(name, side_type):
    n = name.lower()
    # Dips
    if 'truffle' in n: return 'https://unsplash.com/photos/a-bowl-of-food-on-a-wooden-table-T3lfuNL7iLM'
    if 'bbq' in n: return 'https://unsplash.com/photos/lettuce-radishes-and-hotdogs-on-a-wire-rack-w416BDSQnVc'
    if 'cheddar' in n: return 'https://unsplash.com/photos/lettuce-radishes-and-hotdogs-on-a-wire-rack-w416BDSQnVc'
    if 'classic' in n and side_type == 'dip': return 'https://unsplash.com/photos/fried-food-on-white-plastic-container-Mzi4fdo93xQ'
    if 'spicy' in n and side_type == 'dip': return 'https://unsplash.com/photos/red-chili-and-white-garlic-xgsjxQeYppE'
    # Sides
    if 'fish' in n: return 'https://images.unsplash.com/photo-1519984388953-d2406bc725e1?w=300&q=80'
    if 'nugget' in n or 'chicken' in n: return 'https://images.unsplash.com/photo-1562802378-063ec186a863?w=300&q=80'
    if 'mozzarella' in n or 'mozzerella' in n: return 'https://images.unsplash.com/photo-1541745537411-b8046dc6d66c?w=300&q=80'
    if 'chilli' in n or 'chili' in n: return 'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=300&q=80'
    if 'churros' in n: return 'https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=300&q=80'
    if 'salat' in n or 'salad' in n or 'caprese' in n: return 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=300&q=80'
    return 'https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=300&q=80'


def menu(request):
    pizzas = Pizza.objects.all()
    drinks = Drink.objects.all()
    sides = Side.objects.filter(side_type__in=['nuggets', 'mozzarella', 'churros', 'chilli', 'salad'])
    dips = Side.objects.filter(side_type='dip')

    for pizza in pizzas:
        pizza.fallback_image = get_pizza_image(pizza.name)

    for drink in drinks:
        drink.display_image = get_drink_image(drink.name)

    for side in sides:
        side.display_image = get_side_image(side.name, side.side_type)

    for dip in dips:
        dip.display_image = get_side_image(dip.name, dip.side_type)

    return render(request, 'orders/menu.html', {
        'pizzas': pizzas,
        'drinks': drinks,
        'sides': sides,
        'dips': dips,
    })


from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user = User.objects.create_user(
            username=username, password=password,
            first_name=first_name, last_name=last_name, email=email
        )
        return redirect('login')
    return render(request, 'orders/register.html')


@login_required
def add_pizza_to_cart(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    if request.method == 'POST':
        size = request.POST.get(f'pizza_{pizza.id}-size', 'S')
        quantity = int(request.POST.get(f'pizza_{pizza.id}-quantity', 1))
        dietary = request.POST.get(f'pizza_{pizza.id}-dietary', '')
        if size == 'S': price = float(pizza.price_small)
        elif size == 'M': price = float(pizza.price_medium)
        else: price = float(pizza.price_large)
        cart = request.session.get('cart', [])
        cart.append({'type': 'pizza', 'id': pizza.id, 'name': pizza.name,
                     'size': size, 'quantity': quantity, 'dietary': dietary,
                     'price': price, 'subtotal': price * quantity})
        request.session['cart'] = cart
    return redirect('menu')


@login_required
def add_drink_to_cart(request, drink_id):
    drink = get_object_or_404(Drink, id=drink_id)
    if request.method == 'POST':
        quantity = int(request.POST.get(f'drink_{drink.id}-quantity', 1))
        price = float(drink.price)
        cart = request.session.get('cart', [])
        cart.append({'type': 'drink', 'id': drink.id, 'name': drink.name,
                     'quantity': quantity, 'price': price, 'subtotal': price * quantity})
        request.session['cart'] = cart
    return redirect('menu')


@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['subtotal'] for item in cart)
    return render(request, 'orders/cart.html', {'cart': cart, 'total': total})


@login_required
def remove_from_cart(request, item_index):
    cart = request.session.get('cart', [])
    if 0 <= item_index < len(cart):
        cart.pop(item_index)
        request.session['cart'] = cart
    return redirect('view_cart')


@login_required
def clear_cart(request):
    request.session['cart'] = []
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
            order = Order.objects.create(user=request.user, total_price=total,
                                         status='P', delivery_address=delivery_address)
            for item in cart:
                if item['type'] == 'pizza':
                    pizza = get_object_or_404(Pizza, id=item['id'])
                    OrderItem.objects.create(order=order, pizza=pizza, drink=None,
                                             quantity=item['quantity'], size=item['size'],
                                             dietary=item.get('dietary', ''))
                elif item['type'] == 'drink':
                    drink = get_object_or_404(Drink, id=item['id'])
                    OrderItem.objects.create(order=order, pizza=None, drink=drink,
                                             quantity=item['quantity'], size=None)
            request.session['cart'] = []
            return redirect('menu')
    else:
        form = CheckoutForm()
    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart, 'total': total})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'orders/order_history.html', {'orders': orders})
