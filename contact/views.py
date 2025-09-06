from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import os

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact = serializer.save()

        try:
            send_mail(
                subject=f"New contact from {contact.name}",
                message=f"Message:\n{contact.message}\nEmail: {contact.email}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[os.getenv("ADMIN_EMAIL", settings.DEFAULT_FROM_EMAIL)],
                fail_silently=False,
            )
        except Exception as e:
            print("⚠️ Email failed:", e)

        return Response(
            {"message": "Your message has been sent!"},
            status=status.HTTP_201_CREATED,
        )
