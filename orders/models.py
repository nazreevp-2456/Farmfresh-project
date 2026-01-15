from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_orders'
    )
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    # ✅ Invoice PDF file
    invoice = models.FileField(
        upload_to='invoices/',
        null=True,
        blank=True
    )

    # ✅ Prevent duplicate delivery emails
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} → {self.customer.username}"




