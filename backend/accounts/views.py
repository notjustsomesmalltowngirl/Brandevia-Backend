from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def create_temp_superuser(request):
    User = get_user_model()

    if User.objects.filter(email="admin@gmail.com").exists():
        return Response({"status": "exists"})

    User.objects.create_superuser(
        email="admin@gmail.com",
        password="123admin123",
        username='admin'
    )

    return Response({"status": "created"})