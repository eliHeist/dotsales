from django.core.management.base import BaseCommand
from accounts.c_auth.models import CGroup


class Command(BaseCommand):
    help = "initializes the base auth models"

    def handle(self, *args, **options):
        return super().handle(*args, **options)