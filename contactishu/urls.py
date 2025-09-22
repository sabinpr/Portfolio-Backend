from django.urls import path
from .views import ContactMessageCreateView


urlpatterns = [
    path(
        "contact-ishu/",
        ContactMessageCreateView.as_view(),
        name="contact-create-ishu",
    ),
]
