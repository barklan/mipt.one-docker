from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


import re
import os


# from physics.views import COVERAGE_TOTALS


def mainpage(request):
    context = {"navbar": None}
    return render(request, "mainpage/index.html", context)


# def pony_redirect(request):
#     response = redirect("https://blog.neuralpony.com/")
#     return response


# def docs_upload(request):
#     if request.method == "POST":
#         try:
#             doc = str(request.POST["doc"])
#             path = "/home/app/web/mediafiles/docs/index.html"
#             # fs = FileSystemStorage(location=folder)
#             with open(path, "w") as f:
#                 f.write(doc)
#             diditwork = 1
#         except:
#             diditwork = 0
#         response = {
#             "diditwork": diditwork,
#         }
#         return JsonResponse(response)

