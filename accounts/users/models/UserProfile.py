from django.db import models
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="profile")
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="users")
    accessible_branches = models.ManyToManyField("companies.Branch", blank=True)

    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    middle_name = models.CharField(max_length=25, blank=True, null=True)

    phone_1 = models.CharField(_("Phone 1"), max_length=15, blank=True, null=True)
    phone_2 = models.CharField(_("Phone 2"), max_length=15, blank=True, null=True)


    # If accessible_branches is empty → user has access to all branches in their company.
    # If populated → user only sees those branches.
    def has_branch_access(self, branch):
        return self.accessible_branches.filter(id=branch.id).exists() or self.accessible_branches.count() == 0
    
    def __str__(self):
        return f"Profile of {self.user.username} in {self.company.name}"
