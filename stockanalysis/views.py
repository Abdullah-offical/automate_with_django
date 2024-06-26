from django.shortcuts import render
from dal import autocomplete
from .models import Stock
from .forms import StockForm

def stocks(request):
    if request.method =='POST':
        return
    else:
        form = StockForm
        context = {
            'form' : form,
        }
    return render(request, 'stockanalysis/stocks.html', context)


class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Stock.objects.all()

        if self.q:
            print('entered keyword=>', self.q)
            qs = qs.filter(name__istartswith=self.q)
            print('result==>', qs)
        return qs
