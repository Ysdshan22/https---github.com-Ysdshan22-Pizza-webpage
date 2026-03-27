from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)
    available_toppings = models.ManyToManyField('Topping', blank=True)

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=100)
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Drink(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('PR', 'Preparing'),
        ('D', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField()

    #  FIX: size is optional 
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, null=True, blank=True)

    toppings = models.ManyToManyField(Topping, blank=True)

    def clean(self):
        #  Both selected
        if self.pizza and self.drink:
            raise ValidationError("Choose either pizza or drink, not both.")

        #  None selected
        if not self.pizza and not self.drink:
            raise ValidationError("You must select either pizza or drink.")

        #  Pizza MUST have size
        if self.pizza and not self.size:
            raise ValidationError("Pizza must have a size.")

        #  Drink should NOT have size
        if self.drink and self.size:
            raise ValidationError("Drinks should not have a size.")

        #  Drink cannot have toppings (safe check)
        if self.drink and self.pk and self.toppings.exists():
            raise ValidationError("Drinks cannot have toppings.")

    def __str__(self):
        return f"Item {self.id}"