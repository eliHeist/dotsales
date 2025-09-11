from django.db import models

class StockBatch(models.Model):
    branch = models.ForeignKey("companies.Branch", on_delete=models.CASCADE, related_name="batches")
    product = models.ForeignKey("products.BranchProduct", on_delete=models.CASCADE, related_name="batches")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        # unique_together = ("branch", "product", "purchase_date")
        ordering = ['-date']
