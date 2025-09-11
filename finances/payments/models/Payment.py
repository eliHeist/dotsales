from django.db import models
from django.utils import timezone

class Payment(models.Model):
    METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("MOBILE_MONEY", "Mobile Money"),
        ("BANK", "Bank Transfer"),
    ]

    sale = models.ForeignKey("sales.Sale", on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    payment_date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="CASH")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sale.update_status()

    def __str__(self):
        return f"{self.amount} paid on {self.payment_date} for Sale-{self.sale.id}"
