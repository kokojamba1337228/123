from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from .models import Chat, Message, SupportChat, SupportMessage
from properties.models import Property
from polls.models import CustomUser 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.db.models import Q
from django.db.models import Max
from datetime import datetime
from django.views.decorators.http import require_http_methods, require_POST


@login_required
def chat_list(request):
    chats = Chat.objects \
        .filter(Q(buyer=request.user) | Q(seller=request.user)) \
        .annotate(last_message_time=Max('messages__created_at')) \
        .order_by('-last_message_time')
    chat_data = []

    for chat in chats:
        other_user = chat.buyer if request.user == chat.seller else chat.seller
        last_message = chat.messages.last()
        chat_data.append({
            'chat': chat,
            'other_user': other_user,
            'last_message': last_message.content if last_message else "",
            'avatar': other_user.avatar.url if other_user.avatar else None,
            'initial': other_user.first_name[0] if other_user.first_name else (other_user.username[0] if other_user.username else "U"),
        })

    return render(request, 'chat/chat_list.html', {'chats': chat_data})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user != chat.buyer and request.user != chat.seller:
        return HttpResponseNotAllowed(['GET'])

    messages = chat.messages.order_by('created_at')
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})


@login_required
def get_chat_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user != chat.buyer and request.user != chat.seller:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    messages = Message.objects.filter(chat=chat).select_related('sender').order_by('created_at')
    message_list = []
    for msg in messages:
        message_list.append({
            'sender__first_name': msg.sender.first_name if msg.sender.first_name else msg.sender.username,
            'sender__username': msg.sender.username,
            'sender__id': msg.sender.id,
            'content': msg.content,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'sender_avatar': msg.sender.avatar.url if msg.sender.avatar else None, 
        })
    return JsonResponse({'messages': message_list})


@login_required
@csrf_exempt 
def send_message(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id=chat_id)
        if request.user != chat.buyer and request.user != chat.seller:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

        try:
            data = json.loads(request.body)
            content = data.get('content')
            if content:
                Message.objects.create(chat=chat, sender=request.user, content=content)
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'error', 'message': 'Content is empty'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return HttpResponseNotAllowed(['POST'])


@login_required
def create_chat(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    buyer = request.user
    seller = property_obj.owner

    if buyer == seller:
        messages.warning(request, 'Вы не можете начать чат с самим собой.')
        return redirect('property_detail', id=property_obj.id)

    existing_chat = Chat.objects.filter(
        property=property_obj,
        Q(buyer=buyer, seller=seller) | Q(buyer=seller, seller=buyer)
    ).first()

    if existing_chat:
        return redirect('chat_detail', chat_id=existing_chat.id)
    else:
        chat = Chat.objects.create(property=property_obj, buyer=buyer, seller=seller)
        return redirect('chat_detail', chat_id=chat.id)
    
@login_required
@require_POST
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user != chat.buyer and request.user != chat.seller:
        return HttpResponseNotAllowed(['POST']) 

    chat.delete()
    return redirect('chat_list') 


@login_required
@csrf_exempt 
def send_support_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            if not content:
                return JsonResponse({'status': 'error', 'message': 'Content cannot be empty'}, status=400)

            user = request.user
            admin_user = CustomUser.objects.filter(is_staff=True, is_superuser=True).first()
            if not admin_user:
                return JsonResponse({'status': 'error', 'message': 'Admin user not found for support chat'}, status=500)

            support_chat, created = SupportChat.objects.get_or_create(user=user, admin=admin_user)

            SupportMessage.objects.create(chat=support_chat, sender=user, content=content)
            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return HttpResponseNotAllowed(['POST'])


@login_required
def get_support_messages(request):
    user = request.user
    support_chat = SupportChat.objects.filter(user=user).first()

    if not support_chat:
        return JsonResponse({'messages': []})

    messages = SupportMessage.objects.filter(chat=support_chat).select_related('sender').order_by('created_at').values(
        'sender__first_name', 'sender__username', 'sender__id', 'content', 'created_at', 'sender__avatar'
    )
    message_list = []
    for msg in messages:
        sender_name = msg['sender__first_name'] if msg['sender__first_name'] else msg['sender__username']
        message_list.append({
            'sender__first_name': sender_name,
            'sender__id': msg['sender__id'],
            'content': msg['content'],
            'created_at': msg['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            'sender_avatar': msg['sender__avatar'].url if msg['sender__avatar'] else None, 
            'is_admin': CustomUser.objects.get(id=msg['sender__id']).is_staff 
        })
    return JsonResponse({'messages': message_list})


@staff_member_required
def admin_dashboard(request):
    chats = SupportChat.objects.all().order_by('-created_at')
    return render(request, 'chat/admin_dashboard.html', {'chats': chats})


@staff_member_required
def admin_chat_detail(request, chat_id):
    chat = get_object_or_404(SupportChat, id=chat_id)

    messages = chat.messages.order_by('created_at')
    return render(request, 'chat/admin_chat_detail.html', {'chat': chat, 'messages': messages})


@staff_member_required
@csrf_exempt 
def admin_send_message(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(SupportChat, id=chat_id)
        try:
            data = json.loads(request.body)
            content = data.get('content')
            if content:
                SupportMessage.objects.create(chat=chat, sender=request.user, content=content)
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'error', 'message': 'Content is empty'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return HttpResponseNotAllowed(['POST'])


@staff_member_required
def get_admin_chat_messages(request, chat_id):
    chat = get_object_or_404(SupportChat, id=chat_id)
    messages = SupportMessage.objects.filter(chat=chat).select_related('sender').order_by('created_at').values(
        'sender__first_name', 'sender__username', 'sender__id', 'content', 'created_at', 'sender__is_staff', 'sender__avatar' # Include avatar
    )
    message_list = []
    for msg in messages:
        sender_name = msg['sender__first_name'] if msg['sender__first_name'] else msg['sender__username']
        message_list.append({
            'sender__first_name': sender_name,
            'sender__id': msg['sender__id'],
            'content': msg['content'],
            'created_at': msg['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            'is_admin': msg['sender__is_staff'],
            'sender_avatar': msg['sender__avatar'].url if msg['sender__avatar'] else None, 
        })
    return JsonResponse({'messages': message_list})


@staff_member_required
@require_POST
def admin_delete_support_chat(request, chat_id):
    chat = get_object_or_404(SupportChat, id=chat_id)
    chat.delete() 
    return redirect('admin_support_dashboard') 