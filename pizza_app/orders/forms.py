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
        queryset=Topping.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Extra Toppings',
    )

    def __init__(self, *args, pizza=None, **kwargs):
        super().__init__(*args, **kwargs)
        if pizza is not None:
            self.fields['toppings'].queryset = pizza.available_toppings.all()
        else:
            self.fields['toppings'].queryset = Topping.objects.all()


class DrinkCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)


class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Karl Johans gate 1, Oslo'}),
    )
