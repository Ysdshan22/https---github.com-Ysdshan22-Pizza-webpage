
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Pizza, Drink, Order, OrderItem, Topping
from .forms import PizzaCartForm, DrinkCartForm, CheckoutForm
from django.contrib import messages

def menu(request):
    pizzas = Pizza.objects.all()
    drinks = Drink.objects.all()

    pizza_data = []
    for pizza in pizzas:
        form = PizzaCartForm(prefix=f"pizza_{pizza.id}")
        form.fields['toppings'].queryset = pizza.available_toppings.all()

        pizza_data.append({
            'pizza': pizza,
            'form': form,
        })

    drink_forms = {}
    for drink in drinks:
        drink_forms[drink.id] = DrinkCartForm(prefix=f"drink_{drink.id}")

    return render(request, 'orders/menu.html', {
        'pizza_data': pizza_data,
        'drinks': drinks,
        'drink_forms': drink_forms,
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
    form = PizzaCartForm(request.POST, prefix=f"pizza_{pizza.id}")
    form.fields['toppings'].queryset = pizza.available_toppings.all()

    if form.is_valid():
        size = form.cleaned_data['size']
        quantity = form.cleaned_data['quantity']
        toppings = form.cleaned_data['toppings']

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
        cart.append({
            'type': 'pizza',
            'id': pizza.id,
            'name': pizza.name,
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

        messages.success(request, "Drink added to cart successfully.")

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
                        quantity=item['quantity'],
                        size=item['size']
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
                        quantity=item['quantity'],
                        size=None
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