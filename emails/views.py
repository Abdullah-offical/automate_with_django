from django.shortcuts import render, redirect, get_object_or_404

from .tasks import send_email_task
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Email, Subscriber
from django.db.models import Sum


def email_send(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            # send email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            
            # Access the selected email list
            email_list = email.email_list
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
            if email.attachment:
                # tack email attachmenet to path of email file
                attachment = email.attachment.path 
            else:
                attachment = None

            email_id = email.id

            #handover a success message with use celery
            send_email_task.delay(mail_subject, message, to_email, attachment, email_id)

            #without celery send email
            # send_email_notification(mail_subject, message, to_email, attachment)



            # Display a success message
            messages.success(request, 'Email Send Successfully!')
            return redirect('email_send')
    else:
        email = EmailForm()
        context = {
            'email_form' : email
        }
    return render(request, 'emails/email-send.html', context)


def track_click(request):
    return 

def track_open(request):
    return

def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')) # create new field name total send from Sent model
    context = {
        'emails' : emails
    }
    return render(request, 'emails/track_dashboard.html', context)

def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    context = {
        'email' : email
    }
    return render(request, 'emails/track_stats.html', context)