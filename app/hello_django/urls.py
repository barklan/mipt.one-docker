from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from mainpage.views import mainpage
from physics.views import redirect_view, phys, resistor_solver, phgo
from upload.views import image_upload
from antiplag.views import antiplagapi, antiplagpage
from detection.views import detection_page, detect, image_upload_fuck


urlpatterns = [
    path("", mainpage, name="mainpage"),
    path("phys/", phys, name="phys"),
    path("physics/", phgo, name="physics"),
    path("antiplag/", antiplagpage, name="antiplag"),
    path("antiplagapi/", antiplagapi, name="antiplagapi"),
    path("upload/", image_upload, name="upload"),
    path("resistorsolver/", resistor_solver, name="resistorsolver"),
    # path("up/", image_upload, name="upload"),
    path("admin/", admin.site.urls),
    path("detection/", detection_page, name="detection"),
    path("uploadfuck/", image_upload_fuck, name="uploadfuck"),
    path("detect/", detect, name="detect"),
]


if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
