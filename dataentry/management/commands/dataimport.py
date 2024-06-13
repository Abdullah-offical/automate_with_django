from django.core.management.base import BaseCommand, CommandError

# from dataentry.models import Student
from django.apps import apps
import csv

# Proposed commands -  python manage.py importdata file_path model_name

class Command(BaseCommand):
    help = "Import data from csv files"


    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        # logic goes here
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        # Search for the model acreoss all installed apps

        model = None
        for app_config in apps.get_app_configs():
            # try to search for the model
            try:
                model = apps.get_model(app_config.label, model_name)
                break # stop searching one the model is found
            except LookupError:
                continue # model not found in this app, continue searching in next app.

        
        if not model:
            raise CommandError(f'Model "{model_name}" not found in any app!')

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # print(row)
                model.objects.create(**row)  # **row insrt all row auto match

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))