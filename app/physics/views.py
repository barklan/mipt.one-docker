from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from PIL import Image
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio
import re
import requests
import os


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


def phgo(request):
    return render(request, "physics/index.html")


def image_upload_fuck(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        semup = str(request.POST['semup'])
        zadup = str(request.POST['zadup'])
        try:
            Image.open(image_file)
            folder = '/home/app/web/mediafiles/imgbank/' + semup + '/'
            fs = FileSystemStorage(location=folder)
            name_to_save = zadup + '.jpg'
            filename = fs.save(name_to_save, image_file)
            diditwork = 'Решение выложено'
            errorcode = 0
            
        except:
            diditwork = 'It didnt work. Fuck you'
            errorcode = 1
            # return redirect('https://mipt.one/')


        # return render(request, "physics/index.html")
        response = {
            'sem': semup,
            'zad': zadup,
            'diditwork': diditwork,
            'errorcode': errorcode
        }
        return JsonResponse(response)


def redirect_view(request):
    response = redirect('/staticfiles/old/index.html')
    return response


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
    if os.path.isfile('/home/app/web' + image_url):
        code404 = '0'
    else:
        code404 = '1'

    response = {
        'sem': sem,
        'zad': zad,
        'search_output': kor_output,
        'image_url': image_url,
        'code404' : code404
    }
    return JsonResponse(response)


    # context = {
    #     'search_output': output,
    # }
    # return render(request, 'mainpage/index.html', context)
