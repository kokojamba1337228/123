from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', user_register, name='register'),
    path('log-in/', user_login, name='login'),
    path('log-out/', user_logout, name='logout'), 
    path('profile/', profile_view, name='profile'),
    path('delete-favorite/', delete_favorite, name='delete_favorite'),
    path('delete-property/', delete_property, name='delete_property'),
]