from django.db import models

class SaleItem(models.Model):
    sale = models.ForeignKey("sales.Sale", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.BranchProduct", on_delete=models.CASCADE, related_name="sales")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def line_total(self):
        return self.quantity * self.unit_price
