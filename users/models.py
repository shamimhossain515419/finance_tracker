from django.db import models
from django.contrib.auth.models import AbstractUser 
from .managers import CustomUserManager

# Create your models here.
class UserBalanceManager(models.Manager):
    def create_user_balance(self, user, balance=0.00):
        return self.create(user=user, balance=balance)
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
    )

    username = None  # Remove username field
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Removes username requirement

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserBalance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = UserBalanceManager() 
   

   
