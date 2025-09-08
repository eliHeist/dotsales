from django.db import models

class StockBatch(models.Model):
    branch = models.ForeignKey("companies.Branch", on_delete=models.CASCADE, related_name="batches")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="batches")
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # unique_together = ("branch", "product", "purchase_date")
        ordering = ['-date']
