from django.urls import path
from . import views

urlpatterns = [
    path('email-send/', views.email_send, name='email_send'),
]