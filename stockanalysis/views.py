from django.shortcuts import render

def stocks(request):
    return render(request, 'stockanalysis/stocks.html')
