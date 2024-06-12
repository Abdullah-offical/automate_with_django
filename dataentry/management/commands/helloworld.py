from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This is Print Hello world"

    def handle(self, *args, **kwargs):
        # we write the logic
        self.stdout.write('Hello world')