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


def mainpage(request):
    return render(request, 'mainpage/index.html')


def phys(request):
    sem = request.GET.get('sem', None)
    zad = request.GET.get('zad', None)
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

    response = {
        'search_output': output
    }
    return JsonResponse(response)


    # context = {
    #     'search_output': output,
    # }
    # return render(request, 'mainpage/index.html', context)


# def image_upload(request):
#     if request.method == "POST" and request.FILES["image_file"]:
#         image_file = request.FILES["image_file"]
#         fs = FileSystemStorage()
#         filename = fs.save(image_file.name, image_file)
#         image_url = fs.url(filename)
#         print(image_url)
#         return render(request, "upload.html", {
#             "image_url": image_url
#         })
#     return render(request, "upload.html")


# def redirect_view(request):
#     response = redirect('/staticfiles/old/index.html')
#     return response
