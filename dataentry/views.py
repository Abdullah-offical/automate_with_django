from django.conf import settings
from django.shortcuts import render, redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.core.management import call_command # Triger the command from files

from django.contrib import messages

def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # construct the full path
        relative_path = str(upload.file.url)
        # print('relative path=> ', relative_path)
        base_url = str(settings.BASE_DIR)
        # print('BAse PAth=> ', base_url)

        # concatinate 
        file_path = base_url+relative_path
        # print('Absulate Path =>', file_path)

        # trigger the importdata command

        # call command from view 
        # dataimport already create command in managmenet folder for dataentry
        try:
            call_command('dataimport', file_path, model_name) # dataimport is command and other is arguments 2
            messages.success(request, "Data Import Successfully")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('import_data')

    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/importdata.html', context)
