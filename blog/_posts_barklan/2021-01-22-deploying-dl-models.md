---
layout: post
title: "Deploying PyTorch models in production-like environment"
subtitle: "Serving Detectron2 with Django & Flask with Docker"
author: "Gleb"
header-style: text
lang: en
tags:
  - Python
  - PyTorch
  - Deep Learning
  - Computer Vision
  - Detection
  - Detectron2
  - Django
  - Flask
  - Docker
---

Continuing [1st part](/2021/01/20/detectron2-train/). See **[GitHub repo](https://github.com/barklan/mipt.one-docker)**, **[Live demo](https://mipt.one/detection/)**. You can find telegram bot at **[@miptone_bot](https://t.me/miptone_bot)**

### Motivation

Deep Learning model does nothing for you if you don't know how to serve it.


### Overview

The beauty of this is that **everything here is a Docker container** (except the client, but it can be :/ ) and can be deployed on separate server.

![schema](/img/in-post/post-deploying-dl-models/dl_deployment.svg)

PyTorch models free us from moderating user photos and with the structure provided it balances the load and keeps requests short-lived. Thus it our deployment model is **self-automated and scalable**.

### Django

It is the main app and a controller. It is crucial for it to stay "online". The views.py of detection demo page looks like this:

```python
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
    base_path = "/home/app/web/mediafiles/detection_demo/"
    base_relative_url = "/mediafiles/detection_demo/"
    ocred_string = ""
    detected = False
    ocred = False

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
            second_line = f.readline().strip()
            ocred = True if (second_line == "yes") else False
            ocred_string = f.readline().strip()

    response = {
        "image_url": image_url,
        "detect_image_url": detect_image_url,
        "crop_image_url": crop_image_url,
        "detected": detected,
        "ocred": ocred,
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
        # random_id = "1338"

        try:
            Image.open(image_file)
            folder = "/home/app/web/mediafiles/detection_demo/"
            fs = FileSystemStorage(location=folder)
            name_to_save = random_id + ".jpg"
            filename = fs.save(name_to_save, image_file)
            diditwork = 1
        except:
            diditwork = 0

        if diditwork == 1:
            url = f"http://flask:5000/detectron?random_id={random_id}"
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            success = result["success"]

        response = {
            "random_id": random_id,
            "diditwork": diditwork,
        }
        return JsonResponse(response)
```

Simple frontend page uses:
- bootstrap 5
- JS & JQuery (heavy use of AJAX requests)

### Nginx, Traefik & PostreSQL

Nginx as a proxy server to gunicorn. Traefik to make available through ssl with let's encrypt certs.

### Flask

I did not want to host PyTorch models directly in django as I wanted a way to reload or update them without interrupting Django application and rendering server "offline". So I needed a way to make some sort of "internal server". The idea came from [Deploying with Flask tutorial by PyTorch](https://pytorch.org/tutorials/recipes/deployment_with_flask.html).

Here is the app:

```python
import io
import json
import os
from PIL import Image

from flask import Flask, jsonify, request

from detectron_module import TaskDetectron, BaseDetectron
from resnet_module import BaseResnet8

app = Flask(__name__)


cfg_path = "/home/app/flask/mediafiles/models/cfg.pkl"
weights_path = "/home/app/flask/mediafiles/models/model_final.pth"
task_detector = TaskDetectron(cfg_path, weights_path)
base_detector = BaseDetectron()
base_resnet = BaseResnet8("saved_model")


@app.route("/detectron", methods=['GET', 'POST'])
def run_detectron():
    # Initial setup for output
    random_id = str(request.args.get("random_id", "flask_got_no_id"))
    base_path = "/home/app/flask/mediafiles/detection_demo/"
    detected = False
    ocr_failed = True
    image_path = base_path + random_id + ".jpg"
    detect_image_path = base_path + random_id + "_detect.jpg"
    output_path = base_path + random_id + ".txt"

    solution_status = base_resnet.get_model_output(image_path)
    if not solution_status:
        text_output = "This is not a solution photo at all!"
        img = Image.open(image_path)
        img.save(detect_image_path)
        with open(output_path, "w") as f:
            yes_or_no_detected = "yes" if detected else "no"
            yes_or_no_ocred = "yes" if not ocr_failed else "no"
            to_write = [
                f"{yes_or_no_detected}\n",
                f"{yes_or_no_ocred}\n",
                str(text_output)
            ]
            f.writelines(to_write)
    else:
        task_detector.detect_and_save(random_id)

    return jsonify({"success": True, "solution_status": solution_status})


@app.route("/", methods=["GET"])
def root():
    return jsonify(
        {"msg": "Hi there! You reached flask module!"}
    )


if __name__ == "__main__":
    app.run()
```

### Telegram bot

To demostrate that I can include any arbitrary module in this schema. 