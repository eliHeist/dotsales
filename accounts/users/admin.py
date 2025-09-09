from django.contrib import admin
from .models import UserProfile, User


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    can_delete = False
    verbose_name_plural = "User Profile"

    # def get_queryset(self, request):
    #     return super().get_queryset(request).select_related('company')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
    list_display = ("email", "username", "company", "is_company_admin", "is_active", "is_staff")
    list_filter = ("is_company_admin", "company")
    search_fields = ("email", "username")
    ordering = ("email",)
