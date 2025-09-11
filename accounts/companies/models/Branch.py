from django.db import models
from django.utils.translation import gettext_lazy as _

class Branch(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    phone_1 = models.CharField(_("Phone 1"), max_length=15, blank=True, null=True)
    phone_2 = models.CharField(_("Phone 2"), max_length=15, blank=True, null=True)

    class Meta:
        unique_together = ("company", "name")

    def __str__(self):
        return f"{self.company.name} - {self.name}"
