import csv
from django.apps import apps
from django.core.management.base import BaseCommand, CommandParser
import datetime

# proposed command = python manage.py exportanydata table-name
class Command(BaseCommand):
    help = "Exported from data base any model in csv file"

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Data Exported')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        #search thrpugh all the installed apps for the model
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break # stop exsuting one model in found or app in found
            except LookupError:
                pass
        if not model:
            self.stderr.write(f'Model {model_name} cound not found')
            return
        # fatch the data for database
        data = model.objects.all()

        # generate the timestamp of crunat data and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M_%S")

        #define the csv file name/path
        file_path = f'export_{model_name}_data_{timestamp}.csv'

        # open the scv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # write the csv header
            # we want to print the fields names of the model that we are trying to export
            writer.writerow([field.name for field in model._meta.fields])

            #write the data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])
        self.stdout.write(self.style.SUCCESS('Data exported succesfully'))