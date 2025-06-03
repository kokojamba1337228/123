from django.contrib import admin
from .models import Property, PropertyImage, Tag

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1 
    fields = ('image',) 
    max_num = 10 

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'size', 'owner', 'pcreated_at', 'approved')
    search_fields = ('title', 'description', 'location', 'owner__email')
    list_filter = ('owner', 'price', 'location', 'approved', 'tags')
    ordering = ('-pcreated_at',)
    list_per_page = 10
    inlines = [PropertyImageInline] 
    filter_horizontal = ('tags',)
    list_editable = ('approved',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Property, PropertyAdmin)
