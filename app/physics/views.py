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
import json
import urllib.request
import threading


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


COVERAGE_TOTALS = {
    1: [26, 87, 79, 142, 78, 18, 189, 110, 198, 85, 35, 98, 62, 52],
    2: [103, 24, 52, 85, 76, 88, 83, 78, 50, 159, 90, 64],
    3: [30, 53, 84, 38, 45, 54, 97, 103, 65, 93, 57, 104],
    4: [60, 45, 41, 26, 32, 64, 83, 138, 80, 78, 128],
    5: [52, 54, 52, 55, 57, 80, 65, 69, 43, 98],
}

CAPTCHASECRETKEY = os.environ.get('CAPTCHASECRETKEY', 'none'),


def phys(request):
    kor_output = 'none'
    wrong_input = 0
    code404 = 1
    second_file = 0
    image_url = 'https://mipt.one/staticfiles/images/mipt_logo.png'
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
    

    # MY validation checks:
    if ('.' not in zad) or (len(zad) > 6) or (not re.match(r'\d+\.\d+$', zad)):  # base check
        wrong_input = 1
    else:
        zad1, zad2 = zad.split('.')
        zad1_int, zad2_int = int(zad1), int(zad2)
        if (zad1_int == 0) or (zad1_int > len(COVERAGE_TOTALS[int(sem)])):
            wrong_input = 1
        elif (zad2_int == 0) or (zad2_int > COVERAGE_TOTALS[int(sem)][zad1_int - 1]):
            wrong_input = 1
        else:
            wrong_input = 0

        

    if wrong_input == 0:
        try:
            output_list = asyncio.run(fetch(url))
            output = output_list[0]
            if re.match(r'.*странице', output):
                kor_page = re.search(r'№\d*', output)[0]
                kor_output = zad + ' есть в Корявове на странице ' + kor_page
            elif re.match(r'.*не найдена', output):
                kor_output = zad + ' нет в Корявове :('
            elif re.match(r'Укажите номер задачи корректно!', output):
                wrong_input = 1
            else:
                kor_output = ' '
        except:
            kor_output = 'external server down'

        image_url_naked = '/mediafiles/imgbank/' + sem + '/' + zad
        image_url = image_url_naked + '.jpg'
        if os.path.isfile('/home/app/web' + image_url):
            code404 = 0
            if os.path.isfile('/home/app/web' + image_url_naked + '-2.jpg'):
                second_file = 1
        else:
            code404 = 1
    else:
        kor_output = 'такой задачи нет'

    
    response = {
        'wrong_input': wrong_input,
        'sem': sem,
        'zad': zad,
        'search_output': kor_output,
        'image_url': image_url_naked,
        'code404' : code404,
        'second_file': second_file
    }
    return JsonResponse(response)



def phgo(request):


    def countfiles(dir):
        return len([name for name in os.listdir(dir) if (os.path.isfile(os.path.join(dir, name)) and ('-' not in name))])
    

    fps = ['/home/app/web/mediafiles/imgbank/' + str(i) + '/' for i in range(1, 6)]
    counts = [countfiles(fps[i]) for i in range(5)]
    count1, count2, count3, count4, count5 = counts
    totals = [sum(COVERAGE_TOTALS[i]) for i in range(1, 6)]
    total1, total2, total3, total4, total5 = totals
    coverages = [round(counts[i] / totals[i] * 100) for i in range(5)]
    coverage1, coverage2, coverage3, coverage4, coverage5 = coverages

    # this is freedom percentage
    global_total = sum(totals)
    global_count = sum(counts)
    freedom = round(global_count / global_total * 100)

    context = {
        'count1': count1,
        'total1': total1,
        'coverage1': coverage1,
        'count2': count2,
        'total2': total2,
        'coverage2': coverage2,
        'count3': count3,
        'total3': total3,
        'coverage3': coverage3,
        'count4': count4,
        'total4': total4,
        'coverage4': coverage4,
        'count5': count5,
        'total5': total5,
        'coverage5': coverage5,
        'freedom': freedom,
    }
    return render(request, 'physics/index.html', context)


def image_upload_fuck(request):


    def captchaisgood():
        # get the token submitted in the form
        recaptcha_response = request.POST.get('recaptcha_response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': CAPTCHASECRETKEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(payload).encode()
        req = urllib.request.Request(url, data=data)

        # verify the token submitted with the form is valid
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        if result["score"] < 0.5:
            return False
        else:
            return True
        # result will be a dict containing 'contact' and 'action'.
        # it is important to verify both


    if request.method == "POST" and request.FILES["image_file"]:

        if not captchaisgood:
            return redirect('https://mipt.one/staticfiles/old/index.html')
        else:
            pass

        image_file = request.FILES["image_file"]
        semup = str(request.POST['semup'])
        zadup = str(request.POST['zadup'])
        try:
            Image.open(image_file)
            folder = '/home/app/web/mediafiles/imgbank/' + semup + '/'
            fs = FileSystemStorage(location=folder)
            name_to_save = zadup + '.jpg'
            filename = fs.save(name_to_save, image_file)
            diditwork = 1
        except:
            diditwork = 0
            # return redirect('https://mipt.one/')


        # return render(request, "physics/index.html")
        response = {
            'sem': semup,
            'zad': zadup,
            'diditwork': diditwork,
        }
        return JsonResponse(response)


def redirect_view(request):
    response = redirect('/staticfiles/old/index.html')
    return response

