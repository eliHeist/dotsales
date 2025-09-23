from django.db import models
from django.utils.translation import gettext_lazy as _

class GenderChoices(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")

class UserProfile(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="profile")

    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    middle_name = models.CharField(max_length=25, blank=True, null=True)

    gender = models.CharField(max_length=1, blank=True, null=True, choices=GenderChoices.choices)

    phone_1 = models.CharField(_("Phone 1"), max_length=15, blank=True, null=True)
    phone_2 = models.CharField(_("Phone 2"), max_length=15, blank=True, null=True)

    admin_access = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.email}"
    
    get_full_name = lambda self: f"{self.last_name} {self.first_name} {self.middle_name}"

    get_initials = lambda self: f"{self.last_name[0]}{self.first_name[0]}"
