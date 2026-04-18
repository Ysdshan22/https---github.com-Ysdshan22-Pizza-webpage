from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.city

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Allergen(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    allergens = models.ManyToManyField(Allergen, blank=True)
    is_available = models.BooleanField(default=True)
    discount_percent = models.IntegerField(default=0)

    def discounted_price(self):
        if self.discount_percent > 0:
            return round(self.price * (1 - self.discount_percent / 100), 2)
        return self.price

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.item.name}"