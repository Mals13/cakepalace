from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_from_shops')  # Unique related_name
    shop_name = models.CharField(max_length=255)
    shop_address = models.TextField()
    shop_contact = models.CharField(max_length=20)
    shop_description = models.TextField(blank=True)
    shop_logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Admin approval required
    declined = models.BooleanField(default=False)  # Track declined status


    def __str__(self):
        return self.shop_name
    
    
class Cake(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='cakes')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='cakes/')

    def __str__(self):
        return self.name

    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Processing', 'Processing'),
        ('Confirmed', 'Confirmed'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} - {self.status}"
    
class ReviewManager(models.Manager):
    def get_reviews_for_cake(self, cake_id):
        """
        Fetch reviews for a specific cake.
        """
        return self.filter(cake__id=cake_id).select_related('user', 'cake')

    def get_reviews_for_shop(self, shop_id):
        """
        Fetch all reviews for cakes in a specific shop.
        """
        return self.filter(cake__shop__id=shop_id).select_related('user', 'cake')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    cake = models.ForeignKey('Cake', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=1)  # Rating between 1 and 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.cake.name}"
