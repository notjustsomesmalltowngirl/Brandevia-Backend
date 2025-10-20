from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import MailingListSubscriber, NewsLetter
from .serializers import MailingListSubscriberSerializer, NewsLetterSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime

class SubscribeView(generics.CreateAPIView):
            queryset = MailingListSubscriber.objects.all()
            serializer_class = MailingListSubscriberSerializer
            permission_classes = [AllowAny]

            def perform_create(self, serializer):
                self.subscriber = serializer.save()
                subject = "You've successfully subscribed to brandevia's mailing list!"
                from_email = None  # uses DEFAULT_FROM_EMAIL
                bcc = [self.subscriber.email]
                html_content = render_to_string('email/welcome_email.html', {
                    'year': datetime.now().year,
                })
                text_content = "Thank you for subscribing to brandevia's mailing list."
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=from_email,
                    to=None,
                    bcc=bcc
                )
                email.attach_alternative(html_content, 'text/html')
                email.send(fail_silently=False)

            def create(self, request, *args, **kwargs):
                # run DRF's normal create process (this will call perform_create)
                super().create(request, *args, **kwargs)
                # now return a custom response
                return Response(
                    {
                        "success": True,
                        "message": f"{self.subscriber.email} subscribed successfully! 🎉",
                        "subscriber": {
                            "email": self.subscriber.email,
                        },
                    },
                    status=status.HTTP_201_CREATED
                )


class MailCreateView(generics.CreateAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        news_letter = serializer.save()
        admin_emails = ['peace.100daysofcode@gmail.com']
        subscribers = MailingListSubscriber.objects.all()
        news_letter.recipients = ','.join(admin_emails)
        news_letter.save(update_fields=['recipients'])
        news_letter.bcc_subscribers.set(subscribers)
        html_content = news_letter.message

        bcc = [s.email for s in subscribers]

        try:
            email = EmailMultiAlternatives(
                subject=news_letter.subject,
                body=news_letter.message,
                from_email="peace.100daysofcode@gmail.com",  # or DEFAULT_FROM_EMAIL
                to=admin_emails,  # empty so nobody’s in the "To:" field
                bcc=bcc,  # everyone is hidden in BCC
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            news_letter.status = 'sent'
            news_letter.sent_at = timezone.now()
            news_letter.save(update_fields=['status', 'sent_at', 'updated_at'])
        except Exception as e:
            news_letter.status = 'failed'
            news_letter.error_message = str(e)
            news_letter.save(update_fields=['status', 'error_message', 'updated_at'])
        return news_letter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        news_letter = self.perform_create(serializer)

        response_serializer = self.get_serializer(news_letter)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
