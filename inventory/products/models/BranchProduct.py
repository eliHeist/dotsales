from django.db import models

class BranchProduct(models.Model):
    branch = models.ForeignKey("companies.Branch", on_delete=models.CASCADE, related_name="branch_products")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="branch_products")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("branch", "product")

    def __str__(self):
        return f"{self.product.name} at {self.branch.name}"
