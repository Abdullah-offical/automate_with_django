
from awd_min.celery import app
import time
from django.core.management import call_command
from django.conf import settings
from django.core.mail import EmailMessage
from .utils import generate_csv_path, send_email_notification

@app.task
def celery_test_task():
    time.sleep(10) # simulation of any task that's going to take 10 secounds
    # return "Task executed successfully."

# send email 
    mail_subject = 'Test Subject'
    message = 'This is a test email'
    to_email = settings.DEFAULT_TO_EMAIL
    # helper functions from utils.py
    send_email_notification(mail_subject, message, to_email)
    return 'Email Send successfully'


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('dataimport', file_path, model_name) # dataimport is command and other is arguments 2
        
    except Exception as e:
        raise e
    

    # notify the user by email

    mail_subject = 'Import data'
    message = 'Import Data in Data base'
    to_email = settings.DEFAULT_TO_EMAIL
    # helper functions from utils.py
    send_email_notification(mail_subject, message, [to_email])
    return 'DAta imported successfully.'


@app.task
def export_data_task(model_name):
    try:
        call_command('exportanydata', model_name)   
            # notify the user by email with attachment

            
    except Exception as e:
        raise e
    

    # generate csv file path with helper function
    file_path = generate_csv_path(model_name)
    print("====>", file_path)
        
    mail_subject = 'Export data'
    message = 'Expoert data successful. Plase fine the attachment'
    to_email = settings.DEFAULT_TO_EMAIL
        # helper functions from utils.py
    send_email_notification(mail_subject, message, [to_email], attachment=file_path)
    return 'Export data task excuted successfully'   

