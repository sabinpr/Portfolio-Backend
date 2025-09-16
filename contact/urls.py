from django.urls import path
from .views import ContactMessageCreateView, test_email
from django.http import JsonResponse


def ping(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("contact/", ContactMessageCreateView.as_view(), name="contact-create"),
    path("test-email/", test_email, name="test-email"),
    path("ping/", ping, name="ping"),
]
