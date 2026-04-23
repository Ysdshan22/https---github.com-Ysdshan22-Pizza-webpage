from django.db import models
from django.contrib.auth.models import User


class Topping(models.Model):
    name = models.CharField(max_length=100)
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    CATEGORY_CHOICES = [
        ('bestseller', 'Best Seller'),
        ('discount', 'Discount'),
        ('classic', 'Classic'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField(blank=True)
    allergens = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='classic')
    can_be_vegetarian = models.BooleanField(default=True)
    can_be_vegan = models.BooleanField(default=True)
    can_be_glutenfree = models.BooleanField(default=True)
    can_be_dairyfree = models.BooleanField(default=True)
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='pizzas/', blank=True, null=True)
    available_toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return self.name


class Side(models.Model):
    SIDE_CHOICES = [
        ('nuggets', 'Chicken Nuggets'),
        ('mozzarella', 'Mozzarella Sticks'),
        ('churros', 'Churros'),
        ('chilli', 'Chilli Poppers'),
        ('dip', 'Dip Sauce'),
        ('salad', 'Salad'),
    ]

    name = models.CharField(max_length=100)
    side_type = models.CharField(max_length=20, choices=SIDE_CHOICES, default='dip')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

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

    DIETARY_CHOICES = [
        ('', 'Standard'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('glutenfree', 'Gluten-Free'),
        ('dairyfree', 'Dairy-Free'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.SET_NULL, null=True, blank=True)
    side = models.ForeignKey(Side, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, null=True, blank=True)
    dietary = models.CharField(max_length=20, choices=DIETARY_CHOICES, blank=True, default='')
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"Item {self.id}"