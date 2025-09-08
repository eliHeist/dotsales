from django.db import models

class Branch(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ("company", "name")

    def __str__(self):
        return f"{self.company.name} - {self.name}"
