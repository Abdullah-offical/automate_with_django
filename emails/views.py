from django.shortcuts import render, redirect

from .tasks import send_email_task
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber


def email_send(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            # send email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            
            # Access the selected email list
            email_list = email_form.email_list
            # print(email_list)

            # Extract email addresses from the subscribe model in the selected email list
            subscribers = Subscriber.objects.filter(email_list=email_list)


            to_email = [email.email_address for email in subscribers] # list compresion below for loop
            # to_email = []
            # for email in subscribers:
            #     # email address comes from scribe model fiels 
            #     to_email.append(email.email_address)
            # print("======> ",to_email)
            

            # send attachment
            if email_form.attachment:
                # tack email attachmenet to path of email file
                attachment = email_form.attachment.path 
            else:
                attachment = None


            #handover a success message with use celery
            send_email_task.delay(mail_subject, message, to_email, attachment)

            #without celery send email
            # send_email_notification(mail_subject, message, to_email, attachment)



            # Display a success message
            messages.success(request, 'Email Send Successfully!')
            return redirect('email_send')
    else:
        email_form = EmailForm()
        context = {
            'email_form' : email_form
        }
    return render(request, 'emails/email-send.html', context)
