from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os

from .models import ContactMessage
from .serializers import ContactMessageSerializer


@method_decorator(csrf_exempt, name="dispatch")
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Your message has been sent successfully!"},
            status=status.HTTP_201_CREATED,
        )
