from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(username="lukebord").exists():
           CustomUser.objects.create_superuser("lukebord", "lukebord@mit.edu", "admin")
