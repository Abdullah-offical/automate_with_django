from django.conf import settings
from django.shortcuts import render, redirect
from .utils import check_csv_errors, get_all_custom_models
from uploads.models import Upload
from django.core.management import call_command # Triger the command from files

from django.contrib import messages
from .tasks import import_data_task, export_data_task

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


        # check csv errors
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        # handle the import data task here 
        import_data_task.delay(file_path, model_name)


        # trigger the importdata command

        # call command from view 
        # dataimport already create command in managmenet folder for dataentry
        # try:
        #     call_command('dataimport', file_path, model_name) # dataimport is command and other is arguments 2
        #     messages.success(request, "Data Import Successfully")
        # except Exception as e:
        #     messages.error(request, str(e))

        messages.success(request, 'Your data is being imported, you will be notified ones it is done.')
        return redirect('import_data')

    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/importdata.html', context)


def export_data(request):
    
    if request.method == 'POST':
        model_name = request.POST.get('model_name')
        # call the export data task
        export_data_task.delay(model_name)

        # show message to the user
        messages.success(request, 'Your data is exported, you will be notied one it is done.')
        return redirect('export_data')


        
    else:
        custom_model = get_all_custom_models()
        context = {
            'custom_models' : custom_model
        }
    return render(request, 'dataentry/exportdata.html', context)