from rest_framework import serializers
from .models import MailingListSubscriber, NewsLetter


class MailingListSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingListSubscriber
        fields = ['email']

class NewsLetterSerializer(serializers.ModelSerializer):
    bcc_subscribers = serializers.SlugRelatedField(
        many=True,
        slug_field='email',
        read_only=True
    )
    class Meta:
        model = NewsLetter
        fields = [
            'subject',
            'message',
            'recipients',
            'bcc_subscribers',
            'status',
            'sent_at',
            'error_message',
        ]
        read_only_fields = ['status', 'recipients', 'bcc_subscribers', 'sent_at', 'error_message']
