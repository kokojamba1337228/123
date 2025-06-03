from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyForm
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage, Tag
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Max
from chat.models import Chat 
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q 


def property_detail(request, id):
    property = get_object_or_404(Property, id=id)
    if request.method == 'POST' and 'create_chat' not in request.POST:
        if property.owner == request.user:
            messages.warning(request, 'Вы не можете начать чат с самим собой.')
            return redirect('property_detail', id=property.id)
    if request.method == 'POST' and 'create_chat' in request.POST:
        buyer = request.user
        seller = property.owner
        chat, created = Chat.objects.get_or_create(
            property=property,
            buyer=buyer,
            seller=seller
        )
        return redirect('chat_detail', chat_id=chat.id)

    return render(request, 'properties/property_detail.html', {'property': property})

def about_us(request):
    return render(request, 'properties/about.html')

@login_required
def update_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)

    if property_instance.owner != request.user:
        messages.error(request, "У вас нет прав для редактирования этого объявления.")
        return redirect('property_detail', id=property_instance.id)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            updated_property = form.save(commit=False)
            updated_property.save()
            form.save_m2m()

            new_images = request.FILES.getlist('images')
            for image_file in new_images:
                PropertyImage.objects.create(property=updated_property, image=image_file)

            ids_to_delete_str = request.POST.get('remove_images_ids')
            if ids_to_delete_str:
                ids_to_delete = [int(id_str) for id_str in ids_to_delete_str.split(',') if id_str.isdigit()]
                if ids_to_delete:
                    PropertyImage.objects.filter(id__in=ids_to_delete, property=updated_property).delete()


            messages.success(request, 'Объявление успешно обновлено.')
            return redirect('property_detail', id=updated_property.id)
        else:
            messages.error(request, 'Не удалось обновить объявление. Проверьте правильность заполнения всех полей.')
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, 'properties/update_property.html', {
        'form': form,
        'property': property_instance
    })

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.owner = request.user
            property_instance.save()
            form.save_m2m()

            images = request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(property=property_instance, image=image)

            messages.success(request, 'Объявление отправлено на модерацию.')
            return redirect('property_detail', id=property_instance.id)
        else:
            messages.error(request, 'Не удалось загрузить объявление. Проверьте правильность заполнения всех полей.')
    else:
        form = PropertyForm()

    return render(request, 'properties/add_property.html', {'form': form})

def main_view(request):
    return render(request, 'properties/main.html')


def home_page(request):
    all_tags = Tag.objects.all().order_by('category', 'name')

    grouped_tags = {}
    for tag in all_tags:
        category_name = tag.category if tag.category else "Без категории"
        if category_name not in grouped_tags:
            grouped_tags[category_name] = []
        grouped_tags[category_name].append(tag)


    max_price = Property.objects.aggregate(max_price=Max('price'))['max_price'] or 0

    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', max_price)
    query = request.GET.get('query', '')
    order_by = request.GET.get('order_by', '')
    selected_tags_ids = request.GET.getlist('tags')

    try:
        price_min = float(price_min)
        price_max = float(price_max)
        if price_min > price_max:
            price_min, price_max = price_max, price_min
    except ValueError:
        price_min = 0
        price_max = max_price

    properties = Property.objects.filter(
        price__gte=price_min,
        price__lte=price_max,
        approved=True
    )

    if query:
        properties = properties.filter(title__icontains=query)

    if selected_tags_ids:
        for tag_id in selected_tags_ids:
            properties = properties.filter(tags__id=tag_id)
        properties = properties.distinct()


    if order_by == 'price_asc':
        properties = properties.order_by('price')
    elif order_by == 'price_desc':
        properties = properties.order_by('-price')
    else:
        properties = properties.order_by('-id') 

    paginator = Paginator(properties, 30) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favorite_properties = request.user.favorites.values_list('id', flat=True) if request.user.is_authenticated else []

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'query' not in request.GET and 'tags' not in request.GET:
        html = ""
        for property in page_obj:
            html += f"""
                <div class="property-card">
                    <h3>{property.title}</h3>
                    <p>{property.price} BYN</p>
                    <p>{property.description[:100]}...</p>
                </div>
            """
        return JsonResponse({'html': html})

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()

    return render(request, 'properties/home_page.html', {
        'properties': page_obj.object_list,
        'page_obj': page_obj,
        'favorite_properties': favorite_properties,
        'query': query,
        'price_min': price_min,
        'price_max': price_max,
        'max_price': max_price,
        'order_by': order_by,
        'grouped_tags': grouped_tags,
        'selected_tags': list(map(int, selected_tags_ids)),
        'query_string': query_string,
    })


@require_POST
@login_required 
def toggle_favorite_api(request, property_id):

    try:
        property_obj = get_object_or_404(Property, id=property_id)
    except Http404:
        return JsonResponse({'status': 'not_found', 'message': 'Property not found.'}, status=404)

    if property_obj in request.user.favorites.all():
        request.user.favorites.remove(property_obj)
        status = 'removed'
        message = 'Property removed from favorites.'
    else:
        request.user.favorites.add(property_obj)
        status = 'added'
        message = 'Property added to favorites.'

    return JsonResponse({'status': status, 'message': message})


@require_http_methods(["DELETE"])
@login_required
def remove_favorite(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    request.user.favorites.remove(property)
    return JsonResponse({'success': True})