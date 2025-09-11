from django.db import models

class BranchProduct(models.Model):
    branch = models.ForeignKey("companies.Branch", on_delete=models.CASCADE, related_name="branch_products")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="branch_products")
    is_active = models.BooleanField(default=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        unique_together = ("branch", "product")

    def __str__(self):
        return f"{self.product.name} at {self.branch.name}"
    
    def get_stock(self):
        # return stock omitting irrelevant decimal points ie .00
        return self.stock.normalize()
    
    def get_worth(self):
        return int(self.get_stock() * self.product.unit_price)
