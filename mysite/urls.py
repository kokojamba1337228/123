from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from properties.views import main_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name="main"),
    path('properties/', include('properties.urls')),
    path('chat/', include('chat.urls')),
    path('user/', include('polls.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
