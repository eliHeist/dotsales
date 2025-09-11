from datetime import datetime, date
import json
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
        stock_batches = branch_product.batches.filter(active=True).all().order_by('-date')

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
        cost_str = data.get("cost")
        cost = float(cost_str.replace(",", ""))
        selling_price_str = data.get("selling_price")
        selling_price = float(selling_price_str.replace(",", ""))

        branch_product.batches.create(
            date=date,
            quantity=quantity,
            cost=cost,
            selling_price=selling_price,
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
        cost_str = data.get("cost")
        cost = float(cost_str.replace(",", ""))
        selling_price_str = data.get("selling_price")
        selling_price = float(selling_price_str.replace(",", ""))

        batch = get_object_or_404(branch_product.batches, pk=pk) # branch_product.batches.get(pk=pk)
        batch.date = date
        batch.quantity = quantity
        batch.cost = cost
        batch.selling_price = selling_price
        batch.save()

        return self.get(request, bpk, pk)


class SalesView(LoginRequiredMixin, View):
    def get(self, request, bpk, *args, **kwargs):
        data = request.GET
        if data.get("fetch_form"):
            return self.generate_sale_form(request, bpk, *args, **kwargs)

        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        today = date.today()

        sales = branch.sales.filter(date__year=today.year, date__month=today.month, date__day=today.day).all().order_by('-date')
        total_amount = sum(sale.amount_paid for sale in sales)

        context = {
            'branch': branch,
            'sales': sales,
            'total_amount': int(total_amount)
        }
        
        return render(request, 'branches/sales.html', context)
    

class SalesFormView(LoginRequiredMixin, View):
    def get(self, request, bpk, *args, **kwargs):
        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        products = branch.branch_products.all().prefetch_related('product')

        products_data = []

        for product in products:
            pdt_data = {
                'id': product.id,
                'name': product.product.name,
                'batches': []
            }
            batches = product.batches.filter(active=True).all().order_by('-date')

            if not batches.count():
                continue
            
            for batch in batches:
                pdt_data['batches'].append({
                    'id': batch.id,
                    'date': batch.date.strftime('%Y-%m-%d'),
                    'stock': int(batch.get_available_stock()),
                    'selling_price': int(batch.get_selling_price())
                })
            
            products_data.append(pdt_data)
        
        products_data = json.dumps(products_data).replace('"', "'")


        context = {
            'branch': branch,
            'products_data': products_data
        }
        
        return render(request, 'branches/sales_form.html', context)
