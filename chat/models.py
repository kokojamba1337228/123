from django.db import models
from polls.models import CustomUser
from properties.models import Property

def get_default_buyer():
    return CustomUser.objects.first()

def get_default_seller():
    return CustomUser.objects.first()

def get_admin_user():
    return CustomUser.objects.filter(is_superuser=True).first().pk

class Chat(models.Model):
    buyer = models.ForeignKey(CustomUser, related_name="buyer_chats", on_delete=models.CASCADE, default=get_default_buyer)
    seller = models.ForeignKey(CustomUser, related_name="seller_chats", on_delete=models.CASCADE, default=get_default_seller)
    property = models.ForeignKey(Property, related_name='chats', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat about {self.property.title} between {self.buyer.first_name} and {self.seller.first_name}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.sender.first_name}: {self.content[:50]}..."

class SupportChat(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user_chats', on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(CustomUser, related_name='admin_chats', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Chat between {self.user.email} and Admin"

class SupportMessage(models.Model):
    chat = models.ForeignKey(SupportChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support message from {self.sender.email}: {self.content[:50]}..."