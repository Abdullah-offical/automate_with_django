from django.core.management.base import BaseCommand
from dataentry.models import Student


# we want to add some data to the database using the custom command

class Command(BaseCommand):
    help = 'It will insert data to the database'

    def handle(self, *args, **kwargs):
        # logic goes here
        # add 1 data to the database
        # Student.objects.create(
        #     roll_number='1234',
        #     name='John',
        #     age=20
        # )


        # add multiple data to the database
        dataset = [
            {'roll_number': 1434, 'name': 'Muneer', 'age': 20},
            {'roll_number': 1236, 'name': 'Waleed', 'age': 20},
            {'roll_number': 1237, 'name': 'Samad', 'age': 20},
            {'roll_number': 1639, 'name': 'Daki', 'age': 24},
        ]

        for data in dataset:

                # add validation for data 
            roll_number = data['roll_number']
            # if roll_number is exist or not 
            existing_record = Student.objects.filter(roll_number=roll_number).exists()

            if not existing_record:
                Student.objects.create(roll_number=data['roll_number'], name=data['name'], age=data['age'])
                self.stdout.write(self.style.SUCCESS(f'Data with roll number {roll_number} inserted successfully'))
            else:
                self.stdout.write(self.style.ERROR(f'Data with roll number {roll_number} is already exist'))


            # without validation use this 
            # Student.objects.create(roll_number=data['roll_number'], name=data['name'], age=data['age'])

        # run command to insert data into database
        # self.stdout.write(self.style.SUCCESS('Data inserted successfully'))