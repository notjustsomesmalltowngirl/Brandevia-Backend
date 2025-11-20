from rest_framework import serializers
from .models import BlogPost

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
        fields = '__all__'
        read_only_fields = ['author', 'updated_by', 'created_at', 'updated_at']

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d %B %Y %H:%M:%S")

    def get_updated_at_formatted(self, obj):
        return obj.updated_at.strftime("%d %B %Y %H:%M:%S")
