from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect


def mainpage(request):
    return render(request, 'mainpage/index.html')


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
