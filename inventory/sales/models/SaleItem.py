from django.db import models

class SaleItem(models.Model):
    sale = models.ForeignKey("sales.Sale", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.BranchProduct", on_delete=models.CASCADE, related_name="sales")
    stock_batch = models.ForeignKey("stock.StockBatch", on_delete=models.CASCADE, related_name="sales", null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)

    def line_total(self):
        return int(self.quantity * self.stock_batch.selling_price)
