from django.core.management.base import BaseCommand

from dataentry.models import Student
import csv

# Proposed commands -  python manage.py importdata file_path

class Command(BaseCommand):
    help = "Import data from csv files"


    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        # logic goes here
        file_path = kwargs['file_path']
        # print(file_path)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # print(row)
                Student.objects.create(**row)  # **row insrt all row auto match

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))