from datetime import datetime, date
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db import transaction


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

        all_sales = branch.sales.all().order_by('-date')

        current_month_sales = all_sales.filter(date__year=today.year, date__month=today.month).all().order_by('-date')
        month_total = sum(sale.amount_paid for sale in current_month_sales)
        month_debt = sum(sale.balance for sale in current_month_sales)

        current_week_sales = all_sales.filter(date__year=today.year, date__week=today.isocalendar()[1]).all().order_by('-date')
        week_total = sum(sale.amount_paid for sale in current_week_sales)
        week_debt = sum(sale.balance for sale in current_week_sales)

        current_day_sales = all_sales.filter(date__year=today.year, date__month=today.month, date__day=today.day).all().order_by('-date')
        day_total = sum(sale.amount_paid for sale in current_day_sales)
        day_debt = sum(sale.balance for sale in current_day_sales)

        sales = branch.sales.filter(date__year=today.year, date__month=today.month, date__day=today.day).all().order_by('-date')
        total_amount = sum(sale.amount_paid for sale in sales)

        context = {
            'branch': branch,
            'sales': all_sales,
            'current_month_sales': current_month_sales,
            'month_total': month_total,
            'month_debt': month_debt,
            'current_week_sales': current_week_sales,
            'week_total': week_total,
            'week_debt': week_debt,
            'current_day_sales': current_day_sales,
            'day_total': day_total,
            'day_debt': day_debt,
            'today': today,
        }
        
        return render(request, 'branches/sales.html', context)
    

class SalesFormView(LoginRequiredMixin, View):
    def get(self, request, bpk, *args, **kwargs):
        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        products = branch.branch_products.all().prefetch_related('product')

        pk = kwargs.get("pk")
        if pk:
            sale_ = branch.sales.get(pk=pk)
            sale = {
                "id": sale_.id,
                "date": sale_.date.strftime('%Y-%m-%d'),
                "sale_items": [],
                "payments": [],
            }

            print(sale_.items.all())
            for sale_item in sale_.items.all():
                sale["sale_items"].append({
                    "id": sale_item.id,
                    "product_id": sale_item.product.id,
                    "batch_id": sale_item.stock_batch.id,
                    "quantity": float(sale_item.quantity),
                })

            for payment in sale_.payments.all():
                sale["payments"].append({
                    "id": payment.id,
                    "payment_amount": int(payment.amount),
                    "payment_method": payment.method,
                    "payment_date": payment.payment_date.strftime('%Y-%m-%d'),
                })
            print(sale)
            sale = json.dumps(sale).replace('"', "'")
        else:
            sale = None

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
            'sale': sale,
            'branch': branch,
            'products_data': products_data
        }
        
        return render(request, 'branches/sales_form.html', context)

    def post(self, request, bpk, *args, **kwargs):
        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        data = request.POST
        print(data)
        print("\n\n")

        sale_id = kwargs.get("pk", None)
        date_str = data.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        item_ids = data.getlist("item_id")
        item_product_ids = data.getlist("item_product_id")
        item_batch_ids = data.getlist("item_batch_id")
        item_quantities = data.getlist("item_quantity")

        print(item_ids, item_product_ids, item_batch_ids, item_quantities)

        payment_ids = data.getlist("payment_id")
        payment_dates = data.getlist("payment_date")
        payment_amounts = data.getlist("payment_amount")
        payment_methods = data.getlist("payment_method")

        with transaction.atomic():
            print("sale")
            # create or update sale
            if sale_id:
                sale = branch.sales.get(pk=sale_id)
                sale.date = date
                sale.save()
            else:
                sale = branch.sales.create(
                    date=date,
                    branch=branch
                )

            print("items")
            # create or update sale items
            for item_id, item_product_id, item_batch_id, item_quantity in zip(item_ids, item_product_ids, item_batch_ids, item_quantities):
                print("\n\n")
                print("Item 1", item_id, item_product_id, item_batch_id, item_quantity)
                if item_id != 'new':
                    sale_item = sale.items.get(pk=item_id)
                    sale_item.product_id = item_product_id
                    sale_item.stock_batch_id = item_batch_id
                    sale_item.quantity = float(item_quantity.replace(",", ""))
                    sale_item.save()
                    continue
                saley = sale.items.create(
                    product_id=item_product_id,
                    stock_batch_id=item_batch_id,
                    quantity=float(item_quantity.replace(",", "")),
                    sale=sale
                )
                print(saley)

            print("payments")
            # create or update sale payments
            for payment_id, payment_date, payment_amount, payment_method in zip(payment_ids, payment_dates, payment_amounts, payment_methods):
                if payment_id != 'new':
                    sale_payment = sale.payments.get(pk=payment_id)
                    sale_payment.payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()
                    sale_payment.amount = float(payment_amount.replace(",", ""))
                    sale_payment.method = payment_method
                    sale_payment.save()
                    continue
                sale.payments.create(
                    payment_date=datetime.strptime(payment_date, "%Y-%m-%d").date(),
                    amount=float(payment_amount.replace(",", "")),
                    method=payment_method,
                    sale=sale
                )

        return redirect(reverse_lazy('branches:sales', kwargs={'bpk': bpk}))
