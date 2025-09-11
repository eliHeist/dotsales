from django.db import models

class StockBatch(models.Model):
    branch = models.ForeignKey("companies.Branch", on_delete=models.CASCADE, related_name="batches")
    product = models.ForeignKey("products.BranchProduct", on_delete=models.CASCADE, related_name="batches")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    date = models.DateField()

    active = models.BooleanField(default=True)

    get_cost = lambda self: int(self.cost)
    get_selling_price = lambda self: int(self.selling_price)

    class Meta:
        # unique_together = ("branch", "product", "purchase_date")
        ordering = ['-date']
    
    def get_qty_sold(self):
        return sum(item.quantity for item in self.sales.all())
    
    def get_amount_sold(self):
        return sum(item.line_total() for item in self.sales.all())
    
    def get_balance(self):
        return self.quantity - self.get_qty_sold()
    
    def get_worth(self):
        return int(self.quantity * self.selling_price)
    
    def get_available_stock(self):
        return self.quantity - self.get_qty_sold()
    
