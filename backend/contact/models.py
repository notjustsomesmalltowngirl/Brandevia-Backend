from django.db import models
from .validators import phone_validator

class ContactMessage(models.Model):
    QUOTE_CHOICES = [
        ('ERP Solutions', 'ERP Solutions'),
        ('IT Outsourcing', 'IT Outsourcing'),
        ('Managed IT Services', 'Managed IT Services'),
        ('Data & Analytics', 'Data & Analytics'),
        ('general', 'General Enquiry'),
    ]

    SERVICE_CHOICES = [
        # ERP
        ('New ERP Implementation', 'New ERP Implementation'),
        ('ERP Integration with Existing Systems', 'ERP Integration with Existing Systems'),
        ('ERP Customization or Module Development', 'ERP Customization or Module Development'),
        ('ERP Maintenance / Support', 'ERP Maintenance / Support'),
        ('ERP Data Migration or Upgrade', 'ERP Data Migration or Upgrade'),

        # Outsourcing
        ('Dedicated IT Team / Staff Augmentation', 'Dedicated IT Team / Staff Augmentation'),
        ('Helpdesk / Technical Support Setup', 'Helpdesk / Technical Support Setup'),
        ('Infrastructure Management', 'Infrastructure Management'),
        ('Full IT Department Outsourcing', 'Full IT Department Outsourcing'),
        ('Short-term Project Outsourcing', 'Short-term Project Outsourcing'),

        # Managed
        ('Network Monitoring and Maintenance', 'Network Monitoring and Maintenance'),
        ('Server Management', 'Server Management'),
        ('Cloud Infrastructure Management', 'Cloud Infrastructure Management'),
        ('Cybersecurity and Compliance', 'Cybersecurity and Compliance'),
        ('Backup and Disaster Recovery', 'Backup and Disaster Recovery'),

        # Analytics
        ('Business Intelligence Dashboard Setup', 'Business Intelligence Dashboard Setup'),
        ('Predictive Analytics Model', 'Predictive Analytics Model'),
        ('Machine Learning Integration', 'Machine Learning Integration'),
        ('Data Cleaning / Pipeline Setup', 'Data Cleaning / Pipeline Setup'),
        ('AI Chatbot / Automation System', 'AI Chatbot / Automation System'),
    ]

    TIMELINE_CHOICES = [
        ('1-2 weeks', '1–2 Weeks'),
        ('1-2 months +', '1–2 Months +'),
        ('flexible', 'Flexible'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[phone_validator])
    company_name = models.CharField(max_length=150, blank=True, null=True)
    get_a_quote = models.CharField(max_length=20, choices=QUOTE_CHOICES, default='general')

    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='General Enquiry')

    project_timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    message = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        default_service_map = {
            'general': 'General Enquiry',
        }

        if not self.get_a_quote or self.get_a_quote == 'general':
            self.service = default_service_map.get(self.get_a_quote)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.email})"
