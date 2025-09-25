from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def status(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("contact.urls")),
    path("api/", include("contactnabin.urls")),
    path("api/", include("contactishu.urls")),
    path("", status, name="status"),
]
