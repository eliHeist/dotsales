from django.db import models
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CGroupManager(models.Manager):
    """
    The manager for the auth's Group model.
    """

    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

    async def aget_by_natural_key(self, name):
        return await self.aget(name=name)


class CGroup(models.Model):
    """
    Groups are a generic way of categorizing users to apply permissions, or
    some other label, to those users. A user can belong to any number of
    groups.

    A user in a group automatically has all the permissions granted to that
    group. For example, if the group 'Site editors' has the permission
    can_edit_home_page, any user in that group will have that permission.

    Beyond permissions, groups are a convenient way to categorize users to
    apply some label, or extended functionality, to them. For example, you
    could create a group 'Special users', and you could write code that would
    do special things to those users -- such as giving them access to a
    members-only portion of your site, or sending them members-only email
    messages.
    """

    name = models.CharField(_("name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        through="CGroupPermissions",
        verbose_name=_("permissions"),
        blank=True,
    )
    description = models.TextField()

    objects = CGroupManager()

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class CGroupPermissions(models.Model):
    group = models.ForeignKey(CGroup, on_delete=models.CASCADE, related_name="cgroup_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        unique_together = (("group", "permission"),)
