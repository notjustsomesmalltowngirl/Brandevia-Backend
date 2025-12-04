from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

# TODO: Add categories, tags and pen_name to BlogPost model
class BlogPost(models.Model):  # TODO: add time for when the blog should be published  i.e allow scheduled posting
    CATEGORY_CHOICES = [
        ('enterprise_stack', 'Enterprise Stack'),
        ('ops_automation', 'Ops & Automation'),
        ('ai_intelligence', 'AI & Intelligence'),
        ('security_trust', 'Security & Trust'),
        ('digital_playbooks', 'Digital Playbooks'),
        ('future_signals', 'Future Signals'),
        ('inside_brandevia', 'Inside Brandevia'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(
        choices=CATEGORY_CHOICES,
        default='enterprise_stack'
    )
    tags = models.JSONField(
        default=list
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog/covers/', blank=True, null=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='updated_blog_posts'
    )
    # scheduled_publish_at = models.DateTimeField(null=True, blank=True)
    # scheduled_delete_at = models.DateTimeField(null=True, blank=True)

    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


