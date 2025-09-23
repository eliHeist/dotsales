from django.db import models
from django.utils import timezone

class Sale(models.Model):
    STATUS_CHOICES = [
        ("PAID", "Paid"),
        ("PARTIALLY_PAID", "Partially Paid"),
        ("CREDIT", "Credit"),
    ]

    branch = models.ForeignKey("companies.Branch", on_delete=models.CASCADE, related_name="sales")

    date = models.DateField(default=timezone.now)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CREDIT")
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Sale"
        verbose_name_plural = "Sales"
        permissions = [
            ("analyze_profit", "Can analyze profit")
        ]

    def __str__(self):
        return f"Sale {self.id} - {self.branch.name} - {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def total_amount(self):
        return sum(item.line_total() for item in self.items.all())

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
    