from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect


def phgo(request):
    return render(request, "physics/index.html")


def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        sem = '1'
        folder = '/home/app/web/mediafiles/imgbank/' + sem + '/'
        fs = FileSystemStorage(location=folder)
        zad = '666'
        name_to_save = zad + '.jpg'
        filename = fs.save(name_to_save, image_file)
        image_url = fs.url(filename)
        # print(image_url)
        return render(request, "physics/upload.html", {
            "image_url": image_url
        })
    return render(request, "physics/index.html")


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'physics/index.html', {
        'form': form
    })


def redirect_view(request):
    response = redirect('/staticfiles/old/index.html')
    return response
