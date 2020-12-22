from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


from googletrans import Translator
import urllib.request
import json


def antiplagapi(request):
    inputtext = str(request.POST['inptext'])
    antiplagmode = str(request.POST.get('antiplagmode', 'no mode passed'))

    translator = Translator(service_urls=['translate.google.com'])

    if antiplagmode == 'mild':
        langs = ['en', 'de', 'ru']
        translation = inputtext
        for lang in langs:
            translation = translator.translate(translation, dest=lang).text
        output = translation
    elif antiplagmode == 'berserk':
        langs = ['no', 'hi', 'en', 'fr', 'ru']
        translation = inputtext
        for lang in langs:
            translation = translator.translate(translation, dest=lang).text
        output = translation
    elif antiplagmode == 'synonym':
        url = 'https://rustxt.ru/api/index.php'
        payload = {
            'method': 'getSynText',
            'text': inputtext,
        }
        data = urllib.parse.urlencode(payload).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        output = result['modified_text']
    else:
        output = 'SERVER ERROR'




    response = {
        'search_output': output,
        'antiplagmode': antiplagmode
    }
    return JsonResponse(response)
