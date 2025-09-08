from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
