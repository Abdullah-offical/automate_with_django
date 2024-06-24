from django.urls import path
from . import views

urlpatterns = [
    path('email-send/', views.email_send, name='email_send'),
    path('track/click/<unique_id>', views.track_click, name='track_click'),
    path('track/open/<unique_id>', views.track_open, name='track_open'),
    path('track/dashboard', views.track_dashboard, name='track_dashboard'),
]