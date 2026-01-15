from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('customer', 'Customer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"






from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"

