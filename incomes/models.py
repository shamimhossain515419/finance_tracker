from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Income(models.Model):
    transaction_type = models.ForeignKey(
        "expense.TransactionType", 
        on_delete=models.CASCADE,
        related_name="incomes"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Accurate for financial data
    description = models.TextField(blank=True, null=True)  # Optional
    date = models.DateField(auto_now_add=True)  # Auto-sets when income is recorded
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_incomes"
    )

    class Meta:
        ordering = ["-date", "-created_at"]  # Orders by latest income first

    def __str__(self):
        return f"{self.transaction_type.name} - {self.amount}"