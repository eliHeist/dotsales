from django.contrib import admin
from .models.UserProfile import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    can_delete = False
    verbose_name_plural = "User Profile"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('company')

