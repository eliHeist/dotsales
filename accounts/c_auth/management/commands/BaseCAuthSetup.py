from django.core.management.base import BaseCommand

from accounts.c_auth.utils.auth import sync_cgroups
from accounts.c_auth.utils.DefaultGroups import groups as DEFAULT_CGROUPS


class Command(BaseCommand):
    help = "initializes the base auth models"

    def handle(self, *args, **options):
        sync_cgroups(DEFAULT_CGROUPS)