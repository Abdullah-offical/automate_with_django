from django.shortcuts import render, redirect
from .forms import CompressImageForm
from PIL import Image
import io
from django.http import HttpResponse

def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']

            compressed_image = form.save(commit=False)  # comit false is tempery data save
            compressed_image.user = user 

            # perform compression
            img = Image.open(original_img)

            output_format = img.format #set format of the image save farmat
            buffer = io.BytesIO()  # image change to bytes
            img.save(buffer, format=output_format, quality=quality) # complete image save
            buffer.seek(0)

            # save the compressed image inside the model
            compressed_image.compressed_img.save(
                f'compressed_{original_img}', buffer
            )

            return redirect('compress')
    else:
        form = CompressImageForm()
        context = {
            'form' : form
        }
        return render(request, 'image_compress/compress.html', context)
