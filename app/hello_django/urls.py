from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from mainpage.views import mainpage, phys
from physics.views import phgo, redirect_view, model_form_upload
from upload.views import image_upload
from antiplag.views import antiplagpage, antiplagapi


urlpatterns = [
    path("", mainpage, name="mainpage"),
    path("phys/", phys, name="phys"),
    path("physics/", phgo, name="physics"),
    path("antiplag/", antiplagpage, name="antiplag"),
    path("antiplagapi/", antiplagapi, name="antiplagapi"),
    path("upload/", image_upload, name="upload"),
    # path("uploadfuck/", model_form_upload, name='model_form_upload'),
    # path("imgbank/", antiplagapi, name="antiplagapi"),
    # path("up/", image_upload, name="upload"),
    path("admin/", admin.site.urls),
]


if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
