from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .serializers import BlogPostSerializer
from .models import BlogPost
from rest_framework.viewsets import ModelViewSet
from .permissions import AdminOrReadOnly

class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Save with the author set to the logged-in user
            serializer.save(author=request.user)

            return Response({
                "success": True,
                "message": "Blog post created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            raise ValidationError({"success": False, "message": str(e)})

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            serializer.save(updated_by=request.user)

            return Response({
                "success": True,
                "message": "Blog post updated successfully.",
                "data": serializer.data
            })

        except Exception as e:
            raise ValidationError({"success": False, "message": str(e)})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({
                "success": True,
                "message": "Blog post deleted successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Error deleting blog post: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)