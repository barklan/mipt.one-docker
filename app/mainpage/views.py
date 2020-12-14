from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio
import re


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


def mainpage(request):
    return render(request, 'mainpage/index.html')


def phys(request):
    sem = str(request.GET.get('sem', None))
    zad = str(request.GET.get('zad', None))
    url = f'https://mipt1.ru/1_2_3_4_5_kor.php?sem={sem}&zad={zad}'


    async def fetch_links_and_pass(url: str, session: ClientSession):
        async with session.get(url) as response:
            html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find_all("div", class_="short_content")[0]
        output = div.b.get_text()
        return output


    async def fetch(url):
        async with ClientSession() as session:
            tasks = [asyncio.create_task(fetch_links_and_pass(url, session))]
            output = await asyncio.gather(*tasks)
            return output


    output_list = asyncio.run(fetch(url))
    output = output_list[0]

    if re.match(r'.*странице', output):
        kor_page = re.search(r'№\d*', output)[0]
        kor_output = zad + ' есть в Корявове на странице ' + kor_page
    elif re.match(r'.*не найдена', output):
        kor_output = zad + ' нет в Корявове :('
    elif re.match(r'Укажите номер задачи корректно!', output):
        kor_output = 'это что это за задача такая?'
    else:
        kor_output = ' '

    image_url = '/mediafiles/imgbank/' + sem + '/' + zad + '.jpg'
    # image_url = '/mediafiles/imgbank/8.51.jpg'


    response = {
        'search_output': kor_output,
        'image_url': image_url
    }
    return JsonResponse(response)


    # context = {
    #     'search_output': output,
    # }
    # return render(request, 'mainpage/index.html', context)
