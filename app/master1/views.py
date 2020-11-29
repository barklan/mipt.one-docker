from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def master1(request):
    return render(request, "master1.html")
