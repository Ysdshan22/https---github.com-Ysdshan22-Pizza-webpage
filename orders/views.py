from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Pizza, Drink
from .forms import PizzaCartForm, DrinkCartForm


def menu(request):
    pizzas = Pizza.objects.all()
    drinks = Drink.objects.all()

    pizza_forms = {}
    for pizza in pizzas:
        pizza_forms[pizza.id] = PizzaCartForm(prefix=f"pizza_{pizza.id}")

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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'orders/register.html', {
        'form': form
    })


@login_required
def add_pizza_to_cart(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    form = PizzaCartForm(request.POST, prefix=f"pizza_{pizza.id}")

    if form.is_valid():
        size = form.cleaned_data['size']
        quantity = form.cleaned_data['quantity']

        if size == 'S':
            price = float(pizza.price_small)
        elif size == 'M':
            price = float(pizza.price_medium)
        else:
            price = float(pizza.price_large)

        cart = request.session.get('cart', [])

        cart.append({
            'type': 'pizza',
            'id': pizza.id,
            'name': pizza.name,
            'size': size,
            'quantity': quantity,
            'price': price,
            'subtotal': price * quantity,
        })

        request.session['cart'] = cart

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
            'subtotal': price * quantity,
        })

        request.session['cart'] = cart

    return redirect('menu')


@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['subtotal'] for item in cart)

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'total': total,
    })