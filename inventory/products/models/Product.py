from django.db import models

class Product(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("company", "sku")

    def __str__(self):
        return f"{self.name} ({self.sku})"
