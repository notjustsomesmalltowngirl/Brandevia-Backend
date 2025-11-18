from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics, status
from .serializers import BlogPostSerializer
class ViewOneBlogPost(generics.RetrieveAPIView):
    ...

class ViewAllBlogPosts(generics.ListAPIView):
    ...

class UpdateBlogPosts(generics.UpdateAPIView):
    ...

class CreateBlogPosts(generics.CreateAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser]

class DeleteBlogPosts(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]