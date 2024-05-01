from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/resources/', include('resources.urls')),
    path('api/mining/', include('mining.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
