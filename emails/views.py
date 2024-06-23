from django.shortcuts import render

def email_send(request):
    return render(request, 'emails/email-send.html')
