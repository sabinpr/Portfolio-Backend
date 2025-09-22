from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from threading import Thread
import logging
from django.core.mail import EmailMessage

from .models import ContactMessage
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)


def send_contact_email(contact):
    try:
        email = EmailMessage(
            subject=f"New contact from {contact.name}",
            body=f"Message:\n{contact.message}\nEmail: {contact.email}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        email.send(fail_silently=False)
        logger.info("✅ Email sent successfully for contact ID: %s", contact.id)
    except Exception as e:
        logger.error("⚠️ Email failed for contact ID %s: %s", contact.id, e)


class ContactMessageCreateView(generics.CreateAPIView):
    """
    API view to create a contact message and send an email asynchronously.
    """

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact = serializer.save()
        # Use daemon thread to avoid blocking response
        Thread(target=send_contact_email, args=(contact,), daemon=True).start()
        return contact

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = self.perform_create(serializer)
        return Response(
            {
                "message": "Your message has been received. We'll contact you soon!",
                "contact_id": contact.id,
            },
            status=status.HTTP_201_CREATED,
        )
