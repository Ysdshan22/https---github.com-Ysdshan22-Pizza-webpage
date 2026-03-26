from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Pizza, Drink


def menu(request):
    pizzas = Pizza.objects.all()
    drinks = Drink.objects.all()

    return render(request, 'orders/menu.html', {
        'pizzas': pizzas,
        'drinks': drinks
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