from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


from googletrans import Translator


def antiplagapi(request):
    inputtext = str(request.POST['inptext'])
    antiplagmode = str(request.POST.get('antiplagmode', 'no mode passed'))

    translator = Translator(service_urls=['translate.google.com'])

    if antiplagmode == 'mild':
        langs = ['en', 'de', 'ru']
    else:
        langs = ['no', 'hi', 'en', 'fr', 'ru']

    translation = inputtext
    for lang in langs:
        translation = translator.translate(translation, dest=lang).text
    output = translation


    response = {
        'search_output': output,
        'antiplagmode': antiplagmode
    }
    return JsonResponse(response)
