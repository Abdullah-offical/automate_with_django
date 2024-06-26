from django.urls import path
from . import views

urlpatterns = [
    path('stock/', views.stocks, name='stocks'),
    path('stock-autocomplete/', views.StockAutocomplete.as_view(), name='stock_autocomplete'),
]