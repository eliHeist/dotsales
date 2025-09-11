from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from accounts.companies.models import Branch
from accounts.users.models import UserProfile
# Create your views here.
class LandingPageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'company/landing.html', {})
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        if not user.is_company_admin:
            return self.get(request, *args, **kwargs)
        
        company = user.company

        pk = data.get("pk")
        name = data.get("branch_name")
        location = data.get("location")
        email = data.get("email")
        phone_1 = data.get("phone_1")
        phone_2 = data.get("phone_2")

        with transaction.atomic():
            if pk:
                branch = Branch.objects.get(pk=pk)
                branch.name = name
                branch.location = location
                branch.email = email
                branch.phone_1 = phone_1
                branch.phone_2 = phone_2
                branch.save()
            else:
                Branch.objects.create(
                    company=company,
                    name=name,
                    location=location
                )

        return self.get(request, *args, **kwargs)


class UsersListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        company = user.company

        users = company.users.all().prefetch_related("profile")

        context = {
            "users": users
        }
        
        return render(request, 'company/users.html', context)
    

    def post(self, request, *args, **kwargs):
        user = request.user
        company = user.company

        data = request.POST
        pk = data.get("pk")

        first_name = data.get("first_name")
        middle_name = data.get("middle_name")
        last_name = data.get("last_name")
        gender = data.get("gender")
        phone_1 = data.get("phone_1")
        phone_2 = data.get("phone_2")
        is_company_admin = True if data.get("is_company_admin") == "on" else False
        
        accessible_branches_list = data.getlist("accessible_branches")
        accessible_branches = company.branches.filter(pk__in=accessible_branches_list)

        email = data.get("email")
        username = data.get("username")

        with transaction.atomic():
            if pk:
                user = company.users.get(pk=pk)
                

                if not is_company_admin and user.is_company_admin and company.users.filter(is_company_admin=True).count() < 2:
                    is_company_admin = True

                user.email = email
                user.username = username
                user.is_company_admin=is_company_admin
                user.save()

                user.profile.first_name = first_name
                user.profile.middle_name = middle_name
                user.profile.last_name = last_name
                user.profile.gender = gender
                user.profile.phone_1 = phone_1
                user.profile.phone_2 = phone_2
                user.profile.save()
            else:
                # generate a random password
                password = "password"
                
                user = company.users.create_user(
                    email=email,
                    password=password,
                    username=username,
                    is_company_admin=is_company_admin,
                    company=company
                )
                UserProfile.objects.create(
                    user=user,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    gender=gender,
                    phone_1=phone_1,
                    phone_2=phone_2
                )
            
            user.accessible_branches.set(accessible_branches)
        
        return self.get(request, *args, **kwargs)


class ProductListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        company = user.company

        products = company.products.all()
        branches = company.branches.all()

        for branch in branches:
            # get branch product ids
            ids = [b.product.id for b in branch.branch_products.all()]
            branch.product_ids = ids

        context = {
            "products": products,
            "company_branches": branches
        }
        
        return render(request, 'company/products.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        company = user.company

        data = request.POST
        pk = data.get("pk")
        name = data.get("name")
        product_code = data.get("product_code")
        unit_price_str = data.get("unit_price")
        unit_price = int(unit_price_str.replace(",", ""))
        branch_ids = data.getlist("branch_ids")
        branches = company.branches.filter(pk__in=branch_ids)

        with transaction.atomic():
            if pk:
                product = company.products.get(pk=pk)
                product.name = name
                product.unit_price = unit_price
                product.product_code = product_code
                product.save()
            else:
                product = company.products.create(
                    company=company,
                    name=name,
                    product_code=product_code,
                    unit_price=unit_price
                )
            # update branch products
            for branch in branches:
                product.branch_products.get_or_create(
                    product=product,
                    branch=branch
                )
            # deactivate those not submited
            product.branch_products.exclude(branch__in=branches).update(is_active=False)

        return self.get(request, *args, **kwargs)
