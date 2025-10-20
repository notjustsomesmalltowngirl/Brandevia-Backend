from django.urls import path
from .views import SubscribeView, MailCreateView

urlpatterns = [
    path("subscribe/", SubscribeView.as_view(), name='subscribe'),
    path('send-email/', MailCreateView.as_view(), name='send-email'),
]

