from django.urls import path
from .views import ContactMessageCreateView, test_email

urlpatterns = [
    path("contact/", ContactMessageCreateView.as_view(), name="contact-create"),
    path("test-email/", test_email, name="test-email"),
]
