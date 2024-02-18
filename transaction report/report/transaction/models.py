from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    PAYMENT_MODES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('airel money', 'Airtel Money'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    mode_of_payment = models.CharField(max_length=10, choices=PAYMENT_MODES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    def get_week_number(self):
        return self.date,isocalender()



