from django.core.exceptions import PermissionDenied

class AdminAccessRequiredMixin:
    """
    Mixin to ensure the user has admin_access=True on their profile.
    """

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in.")
        
        if user.is_company_admin:
            return super().dispatch(request, *args, **kwargs)

        # Check profile.admin_access
        if not hasattr(user, 'profile') or not getattr(user.profile, 'admin_access', False):
            raise PermissionDenied("Admin access required.")

        return super().dispatch(request, *args, **kwargs)
