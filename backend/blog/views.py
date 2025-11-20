from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import generics, status
from .serializers import BlogPostSerializer
from .models import BlogPost
from rest_framework.viewsets import ModelViewSet
from .permissions import AdminOrReadOnly

class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AdminOrReadOnly]

