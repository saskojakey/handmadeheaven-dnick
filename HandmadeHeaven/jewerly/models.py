from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Jewerly(models.Model):
    type_choices = [('Love themed', 'Love themed'),
                         ('Religious', 'Religious'),
                         ('Nature', 'Nature'),
                         ('Other', 'Other')]
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    exclusive = models.BooleanField()
    type = models.CharField(max_length=255, choices=type_choices)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    jewerly = models.ForeignKey(Jewerly, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def get_total(self):
        return self.jewerly.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
