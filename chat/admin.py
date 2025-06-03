from django.contrib import admin
from .models import Chat, Message, SupportChat, SupportMessage

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    fields = ('sender', 'content', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'buyer', 'seller', 'created_at')
    search_fields = ('buyer__email', 'seller__email', 'property__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [MessageInline]

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'content', 'created_at')
    search_fields = ('chat__id', 'sender__email', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 1
    fields = ('sender', 'content', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True

class SupportChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'admin', 'created_at')
    search_fields = ('user__email', 'admin__email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [SupportMessageInline]

class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'content', 'created_at')
    search_fields = ('chat__id', 'sender__email', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(SupportChat, SupportChatAdmin)
admin.site.register(SupportMessage, SupportMessageAdmin)