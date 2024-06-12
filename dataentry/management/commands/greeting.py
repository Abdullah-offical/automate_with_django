from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This is greeting command"


    # Proposed commed = python manage.py greeting Join
    # proposed output = Hello, {name} Good Morning
    # parser is for take extra argument in command
    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help="Print the command name")

    def handle(self, *args, **kwargs):
        # we write the logic
        name = kwargs['name']
        greeting = f'Hi, {name} Good Morning'
        self.stdout.write(self.style.SUCCESS(greeting))