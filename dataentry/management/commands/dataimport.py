from django.core.management.base import BaseCommand, CommandError

# from dataentry.models import Student
from django.apps import apps
import csv

from django.db import DataError

from dataentry.utils import check_csv_errors

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
        model = check_csv_errors(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)


        # # Search for the model acreoss all installed apps

        # model = None
        # for app_config in apps.get_app_configs():
        #     # try to search for the model
        #     try:
        #         model = apps.get_model(app_config.label, model_name)
        #         break # stop searching one the model is found
        #     except LookupError:
        #         continue # model not found in this app, continue searching in next app.

        
        # if not model:
        #     raise CommandError(f'Model "{model_name}" not found in any app!')
        

        # # compare csv header with model's field names
        # # get all the fields names of the model we found
        # model_fields = [field.name for field in model._meta.fields if field.name != 'id'] # exculade id
        # print(model_fields)

        # with open(file_path, 'r') as file:
        #     reader = csv.DictReader(file)
        #     csv_header = reader.fieldnames

        #     # compare csv header with model's fields names
        #     if csv_header != model_fields:
        #         raise DataError(f"CSV file doesn't match with the {model_name} table fields.")
            for row in reader:
                # print(row)
                model.objects.create(**row)  # **row insrt all row auto match

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))