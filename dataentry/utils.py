from django.apps import apps
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