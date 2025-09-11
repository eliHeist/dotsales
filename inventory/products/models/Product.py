from django.db import models

class Product(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=50, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        verbose_name_plural = "Products"
        # unique_together = ("company", "product_code")

    def __str__(self):
        return f"{self.name} ({self.product_code})"
