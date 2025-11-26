from rest_framework import serializers
from .models import BlogPost
from django.utils import timezone

CATEGORY_TAGS = {
    'enterprise_stack': [
        'ERP', 'Systems', 'Architecture', 'Integration', 'Cloud Infrastructure'
    ],
    'ops_automation': [
        'DevOps', 'ITOps', 'CI/CD', 'Automation', 'Monitoring'
    ],
    'ai_intelligence': [
        'AI', 'Machine Learning', 'Data Engineering', 'Analytics', 'NLP'
    ],
    'security_trust': [
        'Cybersecurity', 'Compliance', 'Privacy', 'Risk Management', 'Zero Trust'
    ],
    'digital_playbooks': [
        'Strategy', 'Digital Transformation', 'Best Practices', 'Guides', 'Frameworks'
    ],
    'future_signals': [
        'Trends', 'Innovation', 'Market Analysis', 'Emerging Tech', 'Research'
    ],
    'inside_brandevia': [
        'Company News', 'Team', 'Culture', 'Case Studies', 'Updates'
    ],
}

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    updated_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    created_at_formatted = serializers.SerializerMethodField()
    updated_at_formatted = serializers.SerializerMethodField()
    class Meta:
        model = BlogPost
        fields = [
                "id",
                "author",
                "title",
                "slug",
                "excerpt",
                "category",
                "tag",
                "content",
                "cover_image",
                "created_at_formatted",
                "updated_at_formatted",
                "updated_by",
                "published",
                "published_at",

        ]
        read_only_fields = ['author', 'updated_by', 'created_at', 'updated_at']
    def validate(self, data):
        category = data.get('category')
        tag = data.get('tag')

        if tag and tag not in CATEGORY_TAGS[category]:
            raise serializers.ValidationError({
                "tag": "Invalid tag for this category."
            })
        return data

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d %B %Y %H:%M:%S")

    def get_updated_at_formatted(self, obj):
        return obj.updated_at.strftime("%d %B %Y %H:%M:%S")

    def validate_scheduled_publish_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("Scheduled publish time must be in the future.")
        return value

    def validate_scheduled_delete_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("Scheduled delete time must be in the future.")
        return value

