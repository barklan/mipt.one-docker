from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mainpage.views import mainpage, phys
from physics.views import phgo, redirect_view
from upload.views import image_upload


urlpatterns = [
    path("", mainpage, name="mainpage"),
    path("phys/", phys, name="phys"),
    path("physics/", redirect_view, name="physics"),
    path("up/", image_upload, name="upload"),
    path("admin/", admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
