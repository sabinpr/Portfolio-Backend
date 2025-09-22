from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("contact.urls")),
    path("api/", include("contactnabin.urls")),
    path("api/", include("contactishu.urls")),  # Added contactishu URLs
]
