
from awd_min.celery import app
import time
from django.core.management import call_command
from django.conf import settings
from django.core.mail import EmailMessage

@app.task
def celery_test_task():
    time.sleep(10) # simulation of any task that's going to take 10 secounds
    # return "Task executed successfully."

# send email 
    mail_subject = 'Test Subject'
    message = 'This is a test email'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.DEFAULT_TO_EMAIL
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
    return 'Email Send successfully'


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('dataimport', file_path, model_name) # dataimport is command and other is arguments 2
        
    except Exception as e:
        raise e
    return 'DAta imported successfully.'

