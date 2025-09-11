from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class BranchesView(LoginRequiredMixin, View):
    def get(self, request, bpk):
        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        context = {
            'branch': branch,
        }
        
        return render(request, 'branches/branches.html', context)


class ProductsView(LoginRequiredMixin, View):
    def get(self, request, bpk):
        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        products = branch.branch_products.all().prefetch_related('product')

        context = {
            'branch': branch,
            'products': products,
        }
        
        return render(request, 'branches/products.html', context)
    
class ProductDetailView(LoginRequiredMixin, View):
    def get(self, request, bpk, pk):
        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        branch_product = branch.branch_products.get(pk=pk)

        stock_batches_count = branch_product.batches.count()
        stock_batches = branch_product.batches.all().order_by('-date')[:10]

        context = {
            'branch': branch,
            'branch_product': branch_product,
            'product': branch_product.product,

            'stock_batches_count': stock_batches_count,
            'stock_batches': stock_batches
        }
        
        return render(request, 'branches/product_detail.html', context)
    
    def post(self, request, bpk, pk):
        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        branch_product = branch.branch_products.get(pk=pk)

        action = request.POST.get("action")
        if action == "restock":
            return self.restock(request, bpk, pk, branch_product, branch)
        elif action == "update_stock":
            return self.update_stock(request, bpk, pk, branch_product)
        
        return self.get(request, bpk, pk)
    
    def restock(self, request, bpk, pk, branch_product, branch):
        data = request.POST

        date_str = data.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        quantity_str = data.get("quantity")
        quantity = float(quantity_str.replace(",", ""))

        branch_product.batches.create(
            date=date,
            quantity=quantity,
            branch=branch,
            product=branch_product
        )

        return self.get(request, bpk, pk)
    
    def update_stock(self, request, bpk, pk, branch_product):
        data = request.POST

        pk = data.get("pk")
        date_str = data.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        quantity_str = data.get("quantity")
        quantity = float(quantity_str.replace(",", ""))

        batch = get_object_or_404(branch_product.batches, pk=pk) # branch_product.batches.get(pk=pk)
        batch.date = date
        batch.quantity = quantity
        batch.save()

        return self.get(request, bpk, pk)
