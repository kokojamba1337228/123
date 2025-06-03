from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', home_page, name='home_page'),
    path('add/', add_property, name='add_property'),
    path("about/", about_us, name="about_us"),
    path('detail/<int:id>/', property_detail, name='property_detail'),
    path('update/<int:property_id>/', update_property, name='update_property'),

    path('toggle-favorite/<int:property_id>/', toggle_favorite_api, name='toggle_favorite_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)