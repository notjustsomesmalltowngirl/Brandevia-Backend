from django.db import models

class MailingListSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class NewsLetter(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()  # plain text or HTML
    recipients = models.TextField(help_text="Comma-separated list of admin emails.")
    bcc_subscribers = models.ManyToManyField(
        'MailingListSubscriber',
        related_name='mails_bcced',
        blank=True
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')],
        default='pending'
    )
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} → {self.recipients} ({self.status})"