from django import forms
from .models import Topping


class PizzaCartForm(forms.Form):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    size = forms.ChoiceField(choices=SIZE_CHOICES)
    quantity = forms.IntegerField(min_value=1, initial=1)

    toppings = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class DrinkCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)


class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter delivery address'})
    )