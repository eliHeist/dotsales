from django.contrib.auth.models import Permission
from django.apps import apps
from ..models import CGroup, CGroupPermissions

def sync_cgroups(groups_data):
    """
    Creates or updates CGroups and assigns permissions with descriptions.
    """
    for group_data in groups_data:
        group_name = group_data["name"]
        permissions = group_data["permissions"]

        # Create or update CGroup
        group, _ = CGroup.objects.update_or_create(
            name=group_name,
            defaults={"description": group_name.replace("_", " ").title()}
        )

        for perm_data in permissions:
            code = perm_data["code"]
            description = perm_data["description"]

            # Split into app_label and codename
            try:
                app_label, codename = code.split(".")
            except ValueError:
                print(f"Invalid permission code format: {code}")
                continue

            # Get Permission object
            try:
                permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
            except Permission.DoesNotExist:
                print(f"Permission not found: {code}")
                continue

            # Create or update CGroupPermissions
            CGroupPermissions.objects.update_or_create(
                group=group,
                permission=permission,
                defaults={"description": description}
            )
