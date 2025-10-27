from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import EmailMessage
import os


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        message_instance = serializer.save()

        subject = f"New Contact Message on Brandevia's website from {message_instance.full_name}"
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
        return message_instance  # return the instance for use in `create()`

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            message_instance = self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    "success": True,
                    "message": "Your message has been sent successfully. We'll get back to you shortly!",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )

        except ValidationError as exc:
            # Clean the validation errors into simple strings
            errors = self._flatten_errors(exc.detail)
            return Response(
                {
                    "success": False,
                    "message": "Please correct the errors below.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "An unexpected error occurred while sending your message. Please try again later.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _flatten_errors(self, detail):
        """
        Convert DRF's nested error structure into a flat, human-readable dict.
        """
        errors = {}
        for field, messages in detail.items():
            if isinstance(messages, (list, tuple)) and messages:
                errors[field] = str(messages[0])
            else:
                errors[field] = str(messages)
        return errors
