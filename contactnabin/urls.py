from django.urls import path
from .views import ContactMessageCreateView


urlpatterns = [
    path(
        "contact-nabin/",
        ContactMessageCreateView.as_view(),
        name="contact-create-nabin",
    ),
]
