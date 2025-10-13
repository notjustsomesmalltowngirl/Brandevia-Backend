from django.urls import path
from .views import SubscribeView, MailCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("subscribe/", SubscribeView.as_view(), name='subscribe'),
    path('send-email/', MailCreateView.as_view(), name='send-email'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

