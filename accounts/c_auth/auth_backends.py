from django.contrib.auth.backends import BaseBackend

class CPermissionBackend(BaseBackend):
    def has_cperm(self, user_obj, perm, obj=None):
        # Skip inactive users
        if not user_obj.is_active:
            return False
        
        if user_obj.is_company_admin:
            return True
        
        if super().has_perm(user_obj, perm, obj):
            return True

    def get_cgroup_permissions(self, user_obj, obj=None):
        for group in user_obj.c_groups.all():
            for perm in group.permissions.all():
                yield f"{perm.content_type.app_label}.{perm.codename}"
    
    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()

        permissions = set(super().get_all_permissions(user_obj, obj))
        permissions.update(self.get_cgroup_permissions(user_obj, obj))
        
        return permissions
