from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)
    available_toppings = models.ManyToManyField('Topping', blank=True, related_name='pizzas')
    emoji = models.CharField(max_length=10, default='🍕')

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
    emoji = models.CharField(max_length=10, default='🥤')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('PR', 'Preparing'),
        ('R', 'Ready for Pickup'),
        ('D', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    delivery_address = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=20, blank=True, default='')
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


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
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, null=True, blank=True)
    toppings = models.ManyToManyField(Topping, blank=True)

    def clean(self):
        if self.pizza and self.drink:
            raise ValidationError("Choose either pizza or drink, not both.")
        if not self.pizza and not self.drink:
            raise ValidationError("You must select either pizza or drink.")
        if self.pizza and not self.size:
            raise ValidationError("Pizza must have a size.")
        if self.drink and self.size:
            raise ValidationError("Drinks should not have a size.")
        if self.drink and self.pk and self.toppings.exists():
            raise ValidationError("Drinks cannot have toppings.")

    def __str__(self):
        return f"Item #{self.id}"


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% off)"


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    opening_hours = models.CharField(max_length=100)
    map_embed_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.name} - {self.city}"
