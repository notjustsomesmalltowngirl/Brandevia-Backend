import os
from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.core.mail import EmailMessage

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        message_instance = serializer.save()

        subject = f"New Contact Message from {message_instance.full_name}"
        message = (
            f"Name: {message_instance.full_name}\n"
            f"Email: {message_instance.email}\n"
            f"Phone: {message_instance.phone}\n"
            f"Company: {message_instance.company_name or 'N/A'}\n"
            f"Get a Quote: {message_instance.get_a_quote}\n"
            f"Service: {message_instance.service}\n"
            f"Project Timeline: {message_instance.project_timeline}\n\n"
            f"Message:\n{message_instance.message}\n"
        )

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=None,
            to=['peace.100daysofcode@gmail.com'],
        )

        if message_instance.attachment:
            attachment_path = message_instance.attachment.path
            if os.path.exists(attachment_path):
                email.attach_file(attachment_path)

        email.send(fail_silently=False)

