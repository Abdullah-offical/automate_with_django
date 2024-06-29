from django.shortcuts import render

def compress(request):
    if request.method == 'POST':
        return
    else:
        return render(request, 'image_compress/compress.html')
