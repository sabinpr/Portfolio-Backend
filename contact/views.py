from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from threading import Thread

from .models import ContactMessage
from .serializers import ContactMessageSerializer


# Function to send email in the background
def send_contact_email(contact):
    try:
        send_mail(
            subject=f"New contact from {contact.name}",
            message=f"Message:\n{contact.message}\nEmail: {contact.email}",
            from_email=settings.DEFAULT_FROM_EMAIL,  # Verified SendGrid email
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        print("✅ Email sent successfully")
    except Exception as e:
        print("⚠️ Email failed:", e)


class ContactMessageCreateView(generics.CreateAPIView):
    """
    API view to create a contact message.
    Sends email asynchronously to avoid worker timeouts.
    """

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        # Save contact message in database
        contact = serializer.save()

        # Send email in a background thread
        Thread(target=send_contact_email, args=(contact,)).start()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"message": "Your message has been sent successfully!"},
            status=status.HTTP_201_CREATED,
        )
