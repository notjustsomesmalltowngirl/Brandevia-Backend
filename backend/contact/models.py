from django.db import models
from .validators import phone_validator

class ContactMessage(models.Model):
    QUOTE_CHOICES = [
        ('erp', 'ERP Solutions'),
        ('outsourcing', 'IT Outsourcing'),
        ('managed', 'Managed IT Services'),
        ('analytics', 'Data & Analytics'),
        ('general', 'General Enquiry'),
    ]

    SERVICE_CHOICES = [
        # ERP
        ('implementation', 'New ERP Implementation'),
        ('integration', 'ERP Integration with Existing Systems'),
        ('customization', 'ERP Customization or Module Development'),
        ('maintenance', 'ERP Maintenance / Support'),
        ('migration', 'ERP Data Migration or Upgrade'),

        # Outsourcing
        ('dedicated', 'Dedicated IT Team / Staff Augmentation'),
        ('helpdesk', 'Helpdesk / Technical Support Setup'),
        ('infrastructure', 'Infrastructure Management'),
        ('full-outsource', 'Full IT Department Outsourcing'),
        ('project', 'Short-term Project Outsourcing'),

        # Managed
        ('network', 'Network Monitoring and Maintenance'),
        ('server', 'Server Management'),
        ('cloud', 'Cloud Infrastructure Management'),
        ('security', 'Cybersecurity and Compliance'),
        ('backup', 'Backup and Disaster Recovery'),

        # Analytics
        ('dashboard', 'Business Intelligence Dashboard Setup'),
        ('predictive', 'Predictive Analytics Model'),
        ('ml', 'Machine Learning Integration'),
        ('pipeline', 'Data Cleaning / Pipeline Setup'),
        ('ai', 'AI Chatbot / Automation System'),
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
    get_a_quote = models.CharField(max_length=15, choices=QUOTE_CHOICES, default='general')
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='General Enquiry')
    project_timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    message = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"
