from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from threading import Thread
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import ContactMessage
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)


# ----------------------------
# Function to send email via SendGrid
# ----------------------------
def send_contact_email(contact):
    """
    Send contact email asynchronously using SendGrid
    """
    try:
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,  # must be verified in SendGrid
            to_emails=[
                settings.ADMIN_EMAIL,
                settings.NABIN_ADMIN_EMAIL,
            ],  # recipient email
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
