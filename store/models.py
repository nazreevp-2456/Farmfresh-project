from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    # ✅ NEW FIELD
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    def __str__(self):
        return self.name
