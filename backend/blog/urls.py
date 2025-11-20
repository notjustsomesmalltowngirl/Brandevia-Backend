from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet

router = DefaultRouter()
router.register(r'blog-post', BlogPostViewSet, basename='blog-post')

urlpatterns = [
    path('', include(router.urls)),
]