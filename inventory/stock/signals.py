from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import StockBatch

@receiver(post_save, sender=StockBatch)
def update_stock(sender, instance:StockBatch, created, **kwargs):
    if created:
        new_amount = float(instance.product.stock) + float(instance.quantity)
        instance.product.stock = new_amount
        instance.product.save()

@receiver(pre_save, sender=StockBatch)
def update_stock_change(sender, instance:StockBatch, **kwargs):
    if instance.pk:
        old_instance = StockBatch.objects.get(pk=instance.pk)

        old_qty = float(old_instance.quantity.normalize())
        new_qty = float(instance.quantity)

        if old_qty == new_qty:
            return
        
        # lets assume it has increased, if it hasn't a negative value will prevail
        increment = new_qty - old_qty
        # product current stock
        pdt_stock = float(instance.product.stock)
        # new product stock
        new_amount = pdt_stock + increment
        instance.product.stock = new_amount
        instance.product.save()

