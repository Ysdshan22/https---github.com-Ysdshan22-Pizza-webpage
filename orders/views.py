from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pizza, Drink, Order, OrderItem, Side
from .forms import PizzaCartForm, DrinkCartForm, CheckoutForm


def get_pizza_image(name):
    n = name.lower()
    if 'margherita' in n: return 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&q=80'
    if 'pepperoni' in n: return 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&q=80'
    if 'picante' in n or 'pikanta' in n: return 'https://images.unsplash.com/photo-1548369937-47519962c11a?w=400&q=80'
    if 'beef' in n: return 'https://unsplash.com/photos/food-photography-of-pizza-with-cheese-mozzarella-parmesan-tomato-basil-7H0NZLbBgyI'
    if 'chicken' in n: return 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=400&q=80'
    if 'nduja' in n: return 'https://unsplash.com/photos/a-pepperoni-pizza-cut-into-slices-on-a-wooden-table-mIESW2fwM3s'
    if 'truffle' in n or 'salami' in n: return 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&q=80'
    if 'tomat' in n: return 'https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=400&q=80'
    if 'devil' in n: return 'https://unsplash.com/photos/baked-pizza-NzHRSLhc6Cs'
    return 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80'


def get_drink_image(name):
    n = name.lower()
    if 'cola' in n or 'coca' in n: return 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=300&q=80'
    if 'fanta' in n: return 'https://unsplash.com/photos/a-can-of-fant-soda-sitting-on-top-of-a-laptop-jsvA222-iaQ'
    if 'pepsi' in n: return 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300&q=80'
    if 'farris' in n or 'water' in n or 'vann' in n: return 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300&q=80'
    if 'solo' in n: return 'https://unsplash.com/photos/a-yellow-can-of-solo-original-lemon-soda-WppbWFTuc1g'
    if 'sprite' in n or 'sprit' in n: return 'https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=300&q=80'
    if 'red bull' in n or 'energy' in n: return 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300&q=80'
    return 'https://images.unsplash.com/photo-1581636625402-29b2a704ef13?w=300&q=80'


def get_side_image(name, side_type):
    n = name.lower()
    if 'truffle' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'bbq' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'cheddar' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'classic' in n and side_type == 'dip': return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'spicy' in n and side_type == 'dip': return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'fish' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'nugget' in n or 'chicken' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'mozzarella' in n or 'mozzerella' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'chilli' in n or 'chili' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'churros' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
    if 'salat' in n or 'salad' in n or 'caprese' in n: return 'https://unsplash.com/photos/a-white-table-topped-with-bowls-filled-with-green-beans-H_0RH4NpIEQ'
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
