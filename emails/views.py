from django.shortcuts import render
from .forms import EmailForm


def email_send(request):
    if request.method == 'POST':
        return
    else:
        email_form = EmailForm()
        context = {
            'email_form' : email_form
        }
    return render(request, 'emails/email-send.html', context)
