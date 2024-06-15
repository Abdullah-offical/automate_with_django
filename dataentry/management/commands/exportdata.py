import csv
from django.core.management.base import BaseCommand
from dataentry.models import Student
import datetime
# propsed command = python manage.py exportdata

class Command(BaseCommand):
    help = 'Export data from Student model to csv a file'

    def handle(self, *args, **kwargs):
        # fatch the data from the data base
        students = Student.objects.all()

        # generate the timestamp of cruent date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M_%S")
        # define the csv file name/path
        file_path = f'exported_students_data_{timestamp}.csv'
        print(file_path)

        #open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # write the csv header
            writer.writerow(['Roll No', 'Name', 'Age'])

            #write the data rows
            for student in students:
                writer.writerow([student.roll_number, student.name, student.age])

        self.stdout.write(self.style.SUCCESS('Data exported successfully'))