from django.db import models
from person.models import User

class Fund(models.Model):
    FUND_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_funds')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=FUND_STATUS_CHOICES, default='ACTIVE')
    image_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'funds'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.current_amount}/{self.target_amount})"

class Donation(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed')
    ]

    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    donation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'donations'
        ordering = ['-donation_date']

    def __str__(self):
        return f"{self.donor.username} donated {self.amount} to {self.fund.title}" 