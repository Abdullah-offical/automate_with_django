from django.shortcuts import render
from .forms import CompressImageForm

def compress(request):
    if request.method == 'POST':
        return
    else:
        form = CompressImageForm()
        context = {
            'form' : form
        }
        return render(request, 'image_compress/compress.html', context)
