from django.urls import path
from .views import SubscribeAPIView, MailCreateAPIView, UnSubscribeAPIView

urlpatterns = [
    path("subscribe/", SubscribeAPIView.as_view(), name='subscribe'),
    path('send-email/', MailCreateAPIView.as_view(), name='send-email'),
    path("unsubscribe/<str:email>/", UnSubscribeAPIView.as_view(), name="unsubscribe"),
]

