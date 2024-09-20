from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Slider(models.Model):
    banner = models.ImageField(upload_to='Media', height_field=None, width_field=None, max_length=None)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    banner = models.ImageField(upload_to='Media', height_field=None, width_field=None, max_length=None)
    title = models.CharField(max_length=500)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Logo(models.Model):
    logo= models.ImageField( upload_to='logo', height_field=None, width_field=None, max_length=None)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each order is linked to a user
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the timestamp when order is created

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Each order has multiple order items
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Each item is linked to a product
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

