from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mainpage.views import mainpage

urlpatterns = [
    path("", mainpage, name="mainpage"),
    path("up/", image_upload, name="upload"),
    path("admin/", admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
