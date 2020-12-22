from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from mainpage.views import mainpage, phgo, antiplagpage
from physics.views import redirect_view, image_upload_fuck, phys
from upload.views import image_upload
from antiplag.views import antiplagapi


urlpatterns = [
    path("", mainpage, name="mainpage"),
    path("phys/", phys, name="phys"),
    path("physics/", phgo, name="physics"),
    path("antiplag/", antiplagpage, name="antiplag"),
    path("antiplagapi/", antiplagapi, name="antiplagapi"),
    path("upload/", image_upload, name="upload"),
    path("uploadfuck/", image_upload_fuck, name='uploadfuck'),
    # path("up/", image_upload, name="upload"),
    path("admin/", admin.site.urls),
]


if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
