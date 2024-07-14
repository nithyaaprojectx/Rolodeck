from django.core.management.base import BaseCommand
from rolodex.models import Person
from django.db import models

class Command(BaseCommand):
    help = 'Finds duplicate code values in Person model'

    def handle(self, *args, **options):
        # Query to find duplicate code values
        duplicate_codes = Person.objects.values('code').annotate(count=models.Count('id')).filter(count__gt=1)

        # Print out duplicate codes if any
        for code in duplicate_codes:
            self.stdout.write(f"Duplicate code: {code['code']}")
