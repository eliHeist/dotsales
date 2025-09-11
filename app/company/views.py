from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.companies.models import Branch
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

        print(name)

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