from django.urls import path
from . import views

urlpatterns = [
    path('chat_list/', views.chat_list, name='chat_list'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('<int:chat_id>/get_messages/', views.get_chat_messages, name='get_chat_messages'), # Новый URL
    path('create/<int:property_id>/', views.create_chat, name='create_chat'),
    path('delete/<int:chat_id>/', views.delete_chat, name='delete_chat'),

    path('support/send/', views.send_support_message, name='send_support_message'),
    path('support/get_messages/', views.get_support_messages, name='get_support_messages'),

    path('admin/support/dashboard/', views.admin_dashboard, name='admin_support_dashboard'),
    path('admin/support/chat/<int:chat_id>/', views.admin_chat_detail, name='admin_chat_detail'),
    path('admin/support/chat/<int:chat_id>/send/', views.admin_send_message, name='admin_send_message'),
    path('admin/support/chat/<int:chat_id>/messages/', views.get_admin_chat_messages, name='get_admin_chat_messages'),
    path('admin/support/chat/<int:chat_id>/delete/', views.admin_delete_support_chat, name='admin_delete_support_chat'),
]