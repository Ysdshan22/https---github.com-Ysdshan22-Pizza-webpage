from django.db import models
from django.contrib.auth.models import User

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)

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
    
from django.contrib.auth.models import User  # make sure this is at top

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=50)
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

    quantity = models.IntegerField()
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)

    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"Item {self.id}"