from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/mailing/', include('mailing.urls')),
    path('api/v1/contact/', include('contact.urls')),
    path('api/v1/blog/', include('blog.urls')),
    path('api/v1/auth/', include('accounts.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)