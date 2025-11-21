from rest_framework import serializers
from .models import BlogPost
from django.utils import timezone

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
                "author",
                "updated_by",
                "created_at_formatted",
                "updated_at_formatted",
                "title",
                "slug",
                "excerpt",
                "content",
                "cover_image",
                "published",
                "published_at",
        ]
        read_only_fields = ['author', 'updated_by', 'created_at', 'updated_at']

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

