from django.db import models
from django.contrib.auth.models import User
from shops.models import Cake


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    cakes = models.ManyToManyField(Cake, through='CartItem', related_name='carts')

    def __str__(self):
        return f"Cart of {self.user.username}"

    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    cakes = models.ManyToManyField(Cake, through='CartItem')

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.cake.name} in {self.cart.user.username}'s cart"
    