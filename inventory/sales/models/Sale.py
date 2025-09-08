from django.db import models
from django.utils import timezone

class Sale(models.Model):
    STATUS_CHOICES = [
        ("PAID", "Paid"),
        ("PARTIALLY_PAID", "Partially Paid"),
        ("CREDIT", "Credit"),
    ]

    branch = models.ForeignKey("companies.Branch", on_delete=models.CASCADE, related_name="sales")

    date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CREDIT")
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Sale {self.id} - {self.branch.name} - {self.date.strftime('%Y-%m-%d')}"

    def calculate_total(self):
        self.total_amount = sum(item.line_total() for item in self.items.all())
        self.save()

    @property
    def amount_paid(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def balance(self):
        return self.total_amount - self.amount_paid

    def update_status(self):
        if self.balance <= 0:
            self.status = "PAID"
        elif self.amount_paid > 0:
            self.status = "PARTIALLY_PAID"
        else:
            self.status = "CREDIT"
        self.save()
    