from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage


from PIL import Image
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio
import re
import os
import json
import urllib.request

from fractions import Fraction

from physics.models import Zad

# import threading


COVERAGE_TOTALS = {
    1: [26, 87, 79, 142, 78, 18, 189, 110, 198, 85, 35, 98, 62, 52],
    2: [103, 24, 52, 85, 76, 88, 83, 78, 50, 159, 90, 64],
    3: [30, 53, 84, 38, 45, 54, 97, 103, 65, 93, 57, 104],
    4: [60, 45, 41, 26, 32, 64, 83, 138, 80, 78, 128],
    5: [52, 54, 52, 55, 57, 80, 65, 69, 43, 98],
}

CAPTCHASECRETKEY = (os.environ.get("CAPTCHASECRETKEY", "none"),)


def phys(request):
    kor_output = "none"
    wrong_input = False
    image_found = False
    second_file = False
    third_file = False
    image_url = None
    image_url_naked = "none"
    sem = str(request.GET.get("sem", None))
    zad = str(request.GET.get("zad", None))

    url = f"https://mipt1.ru/1_2_3_4_5_kor.php?sem={sem}&zad={zad}"

    # async def fetch_links_and_pass(url: str, session: ClientSession):
    #     async with session.get(url) as response:
    #         html = await response.text()
    #     soup = BeautifulSoup(html, "html.parser")
    #     div = soup.find_all("div", class_="short_content")[0]
    #     output = div.b.get_text()
    #     return output

    # async def fetch(url):
    #     async with ClientSession() as session:
    #         tasks = [asyncio.create_task(fetch_links_and_pass(url, session))]
    #         output = await asyncio.gather(*tasks)
    #         return output

    # MY validation checks:
    if (
        ("." not in zad) or (len(zad) > 6) or (not re.match(r"\d+\.\d+$", zad))
    ):  # base check
        wrong_input = True
    else:
        zad1, zad2 = zad.split(".")
        zad1_int, zad2_int = int(zad1), int(zad2)
        if (zad1_int == 0) or (zad1_int > len(COVERAGE_TOTALS[int(sem)])):
            wrong_input = True
        elif (zad2_int == 0) or (zad2_int > COVERAGE_TOTALS[int(sem)][zad1_int - 1]):
            wrong_input = True
        else:
            wrong_input = False

    if wrong_input == False:

        # try:  # try to connect to external to 
        #     output_list = asyncio.run(fetch(url))
        #     output = output_list[0]
        #     if re.match(r".*странице", output):
        #         kor_page = re.search(r"№\d*", output)[0][1:]
        #         kor_output = zad + " есть в Корявове на странице " + kor_page + ". "
        #     elif re.match(r".*не найдена", output):
        #         kor_output = zad + " нет в Корявове :( "
        #     elif re.match(r"Укажите номер задачи корректно!", output):
        #         wrong_input = True
        #     else:
        #         kor_output = " "
        # except:
        #     kor_output = "external server down"
        try:
            page = Zad.objects.get(sem=sem, zad=zad).page
            if page == 0:
                kor_output = zad + " нет в Корявове."
            else:
                kor_output = zad + " есть в Корявове на странице " + str(page) + "."
        except Zad.DoesNotExist:
            page = 0
            kor_output = "entry does not extist in the database"

        image_url_naked = "/mediafiles/imgbank/" + sem + "/" + zad
        image_url = image_url_naked + ".jpg"
        full_image_url = "https://mipt.one" + image_url
        if os.path.isfile("/home/app/web" + image_url):
            image_found = True
            if os.path.isfile("/home/app/web" + image_url_naked + "-2.jpg"):
                second_file = True
                if os.path.isfile("/home/app/web" + image_url_naked + "-3.jpg"):
                    third_file = True
        else:
            image_found = False
            kor_output = kor_output + " Готового решения пока нет :("

        sem_to_name = [
            "",
            "Механика",
            "Термодинамика",
            "Электричесво",
            "Оптика",
            "Атомная",
        ]
        kor_output = sem_to_name[int(sem)] + ". " + kor_output
    else:
        full_image_url = None
        page = 0
        kor_output = "такой задачи нет"

    response = {
        "wrong_input": wrong_input,
        "sem": sem,
        "zad": zad,
        "koryavov_page": page,
        "search_output": kor_output,
        "image_found": image_found,
        "full_image_url": full_image_url,
        "second_file": second_file,
        "third_file": third_file,
        "image_url": image_url_naked,
    }
    return JsonResponse(response)


def image_upload_fuck(request):
    def captchaisgood():
        # get the token submitted in the form
        recaptcha_response = request.POST.get("recaptcha_response")
        url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {"secret": CAPTCHASECRETKEY, "response": recaptcha_response}
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
            return redirect("https://mipt.one/staticfiles/old/index.html")
        else:
            pass

        image_file = request.FILES["image_file"]
        semup = str(request.POST["semup"])
        zadup = str(request.POST["zadup"])
        try:
            Image.open(image_file)
            folder = "/home/app/web/mediafiles/imgbank/" + semup + "/"
            fs = FileSystemStorage(location=folder)
            name_to_save = zadup + ".jpg"
            filename = fs.save(name_to_save, image_file)
            diditwork = 1
        except:
            diditwork = 0
            # return redirect('https://mipt.one/')

        # return render(request, "physics/index.html")
        response = {
            "sem": semup,
            "zad": zadup,
            "diditwork": diditwork,
        }
        return JsonResponse(response)


def redirect_view(request):
    response = redirect("/staticfiles/old/index.html")
    return response


def resistor_solver(request):
    output = "???"

    try:
        R1 = int(request.GET.get("R1", None))
        R2 = int(request.GET.get("R2", None))
        R3 = int(request.GET.get("R3", None))
        R4 = int(request.GET.get("R4", None))
        R5 = int(request.GET.get("R5", None))
    except:
        output = "Неверный ввод :("
        return JsonResponse({"output": output})
    
    Rx1 = Fraction(R3 * R1, R3 + R5 + R1)
    Rx2 = Fraction(R5 * R1, R3 + R5 + R1)
    Rx3 = Fraction(R3 * R5, R3 + R5 + R1)
    Ry1 = Rx2 + R2
    Ry2 = Rx3 + R4
    Rz = Ry1 * Ry2 / (Ry1 + Ry2)
    Rab = Rx1 + Rz

    output = "Rab = " + str(Rab) + " R"

    return JsonResponse({"output": output})
