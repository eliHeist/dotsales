from django.contrib import admin
from .forms import CompanyAdminUserForm
from accounts.users.models.User import User

from .models import Company, Branch

class CompanyUserInline(admin.StackedInline):
    model = User
    form = CompanyAdminUserForm
    extra = 1
    can_delete = False
    verbose_name_plural = "Company Admin User"

    def save_new(self, form, commit=True):
        return form.save(commit=commit, company=self.parent_obj)

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # inlines = [CompanyUserInline]
    list_display = ("name", "contact", "address")

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    # inlines = [CompanyUserInline]
    list_display = ("name", "company", "email")

