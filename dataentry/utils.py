import datetime
import os
from django.core.mail import EmailMessage
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import csv

from django.db import DataError

def get_all_custom_models():
    default_models = ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'Upload', 'User']
    # try to get all the apps
    custom_model = []
    for model in apps.get_models():
        # print(model.__name__)
        if model.__name__ not in default_models:
            custom_model.append(model.__name__)
        
    return custom_model

def check_csv_errors(file_path, model_name):
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
    
    # compare csv header with model's field names
    # get all the fields names of the model we found
    model_fields = [field.name for field in model._meta.fields if field.name != 'id'] # exculade id
    
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

                # compare csv header with model's fields names
            if csv_header != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields.")
    except Exception as e:
        raise e
    return model


def send_email_notification(mail_subject, message, to_email, attachment=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=to_email) # [to_email]
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e
    
def generate_csv_path(model_name):
    # generate the timestamp of crunat data and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M_%S")

        #define the csv file name/path
    export_dir = 'exported_data'
    file_name = f'export_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    print("Dile path==========>", file_path)
    return file_path
    