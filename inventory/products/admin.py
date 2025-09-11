from django.contrib import admin
from .models import Product, BranchProduct

# Register your models here.

admin.site.register(Product)
admin.site.register(BranchProduct)
