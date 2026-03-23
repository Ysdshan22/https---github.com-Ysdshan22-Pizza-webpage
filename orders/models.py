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