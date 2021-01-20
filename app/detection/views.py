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

from detection.detectron import *

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

    if random.choice([i for i in range(10)]) == 0:
        clean_all_collected()
    context = {"hey": None}
    return render(request, "detection/index.html", context)


def detect(request):
    def make_predictor():
        with open("/home/app/web/mediafiles/models/cfg.pkl", "rb") as f:
            cfg = pickle.load(f)

        cfg.MODEL.DEVICE = "cpu"
        cfg.MODEL.WEIGHTS = os.path.join("/home/app/web/mediafiles/models/model_final.pth")
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        predictor1 = DefaultPredictor(cfg)
        return predictor1

    random_id = str(request.GET.get("random_id_req", "shit_no_id"))
    image_url = "/mediafiles/detection_demo/" + str(random_id) + ".jpg"
    detect_image_url = "/mediafiles/detection_demo/" + str(random_id) + "_detect.jpg"
    crop_image_url = "/mediafiles/detection_demo/" + str(random_id) + "_crop.jpg"
    ocred_string = ""

    # init model
    predictor = make_predictor()




    # im = cv2.imread("demo2.jpg")
    im = Image.open("/home/app/web" + image_url)
    orig = im

    # resize initial image to reduce inference time on cpu
    # im = resize(im, 1000)
    im = pil_to_cv(im)

    outputs = predictor(im)  # format is documented at https://detectron2.readthedocs.io/tutorials/models.html#model-output-format
    v = Visualizer(im[:, :, ::-1],
    #                metadata=my_dataset_test_metadata, 
                scale=1, 
    )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    img_det = get_image(out.get_image()[:, :, ::-1])

    img_det.save("/home/app/web" + detect_image_url)


    detected = False

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
        
        try:
            Image.open(image_file)
            folder = "/home/app/web/mediafiles/detection_demo/"
            fs = FileSystemStorage(location=folder)
            name_to_save = random_id + ".jpg"
            filename = fs.save(name_to_save, image_file)
            diditwork = 1
        except:
            diditwork = 0
            # return redirect('https://mipt.one/')

        # return render(request, "physics/index.html")
        response = {
            "random_id": random_id,
            "diditwork": diditwork,
        }
        return JsonResponse(response)
