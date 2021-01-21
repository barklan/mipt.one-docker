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
import random

from fractions import Fraction

import subprocess

# import threading

CAPTCHASECRETKEY = os.environ.get("CAPTCHASECRETKEY")


def detection_page(request):
    def clean_all_collected():
        folder = '/home/app/web/mediafiles/detection_demo'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except:
                pass

    # if random.choice([i for i in range(10)]) == 0:
    #     clean_all_collected()
    context = {"hey": None}
    return render(request, "detection/index.html", context)


def detect(request):
    base_path = "/home/app/web/mediafiles/detection_demo/"
    base_relative_url = "/mediafiles/detection_demo/"
    ocred_string = ""
    detected = False

    random_id = str(request.GET.get("random_id_req", "shit_no_id"))
    image_url = base_relative_url + random_id + ".jpg"
    detect_image_url = base_relative_url + random_id + "_detect.jpg"
    crop_image_url = base_relative_url + random_id + "_crop.jpg"
    output_filename = random_id + ".txt"
    output_path = base_path + output_filename
    
    if os.path.isfile(output_path):
        with open(output_path, "r") as f:
            first_line = f.readline().strip()
            detected = True if (first_line == "yes") else False
            if detected == True:
                ocred_string = f.readline().strip()
            else:
                pass

    response = {
        "image_url": image_url,
        "detect_image_url": detect_image_url,
        "crop_image_url": crop_image_url,
        "detected": detected,
        "ocred_string": ocred_string,
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
        random_id = str(request.POST.get("random_id", "shit_no_id"))
        random_id = "1338"
        

        Image.open(image_file)
        folder = "/home/app/web/mediafiles/detection_demo/"
        fs = FileSystemStorage(location=folder)
        name_to_save = random_id + ".jpg"
        filename = fs.save(name_to_save, image_file)

        # relay to detectron
        # cmd = f"python /home/app/web/detectron.py --id {random_id}"
        # p = subprocess.Popen(cmd, shell=True, close_fds=False)
        # pid = p.pid
        # return redirect('https://mipt.one/')

        # return render(request, "physics/index.html")
        response = {
            "random_id": random_id,
            "diditwork": diditwork,
        }
        return JsonResponse(response)
