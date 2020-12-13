from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from googletrans import Translator


def antiplagpage(request):
    return render(request, "antiplag/index.html")


def antiplagapi(request):
    inputtext = request.GET.get('inptext', None)
    # translator = Translator()

    translator = Translator(service_urls=['translate.google.com'])

    langs = ['no', 'hi', 'en', 'fr', 'ru']

    translation = str(inputtext)
    for lang in langs:
        translation = translator.translate(translation, dest=lang).text


    
    # translation1 = translator.translate(str(inputtext), dest='no').text
    # translation2 = translator.translate(translation1, dest='hi').text
    # translation3 = translator.translate(translation2, dest='ru').text

    output = translation
    # translation4 = translator.translate(translation3, dest='fr').text
    # translation5 = translator.translate(translation4, dest='ru').text
    
    # inputtext = request.POST.get('inptext', None)
    # try:
    #     for key, value in request.POST.items():
    #         inputtext = value
    # except:
    #     inputtext = 'fuck you'

    # url = f'https://mipt1.ru/1_2_3_4_5_kor.php?sem={sem}&zad={zad}'


    # async def fetch_links_and_pass(url: str, session: ClientSession):
    #     async with session.get(url) as response:
    #         html = await response.text()
    #     soup = BeautifulSoup(html, 'html.parser')
    #     div = soup.find_all("div", class_="short_content")[0]
    #     output = div.b.get_text()
    #     return output


    # async def fetch(url):
    #     async with ClientSession() as session:
    #         tasks = [asyncio.create_task(fetch_links_and_pass(url, session))]
    #         output = await asyncio.gather(*tasks)
    #         return output


    # output_list = asyncio.run(fetch(url))
    # output = output_list[0]


    response = {
        'search_output': output
    }
    return JsonResponse(response)
