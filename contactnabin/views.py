from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from threading import Thread
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import ContactMessage
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)


def send_contact_email(contact):
    try:
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=[settings.ADMIN_EMAIL, settings.NABIN_ADMIN_EMAIL],
            subject=f"New contact from {contact.name}",
            html_content=f"<p>{contact.message}</p><p>Email: {contact.email}</p>",
        )
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(
            "✅ Contact email sent for contact ID %s. Status code: %s",
            contact.id,
            response.status_code,
        )
    except Exception as e:
        logger.error("⚠️ Failed to send contact email for ID %s: %s", contact.id, str(e))


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact = serializer.save()
        Thread(target=send_contact_email, args=(contact,), daemon=True).start()
        return contact

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = self.perform_create(serializer)
        return Response(
            {"message": "Your message has been received.", "contact_id": contact.id},
            status=status.HTTP_201_CREATED,
        )
