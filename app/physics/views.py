from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect


def phgo(request):
    return render(request, "physics/index.html")


def redirect_view(request):
    response = redirect('/staticfiles/old/index.html')
    return response
