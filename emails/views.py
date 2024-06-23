from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings


def email_send(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form.save()
            # send email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            to_email = settings.DEFAULT_TO_EMAIL
            send_email_notification(mail_subject, message, to_email)



            # Display a success message
            messages.success(request, 'Email Send Successfully!')
            return redirect('email_send')
    else:
        email_form = EmailForm()
        context = {
            'email_form' : email_form
        }
    return render(request, 'emails/email-send.html', context)
