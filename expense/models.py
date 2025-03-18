from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique name for transaction type
    description = models.TextField(blank=True, null=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        User,
        related_name="created_transaction_types",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_at"]  # Newest first


class Expense(models.Model):
    transaction_type = models.ForeignKey(
        "TransactionType", 
        on_delete=models.CASCADE, 
        related_name="expenses"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Supports large values
    description = models.TextField(blank=True, null=True)  # Optional
    date = models.DateField(auto_now_add=True)  # Stores when the expense was made
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user_expenses"
    )

    class Meta:
        ordering = ["-date", "-created_at"]  # Recent expenses first

    def __str__(self):
        return f"{self.transaction_type.name} - {self.amount}"