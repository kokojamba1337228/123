from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active', 'rating', 'verified', 'user_id')
    list_filter = ('is_staff', 'is_active', 'verified')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'avatar', 'user_id', 'rating', 'verified', 'services')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(CustomUser, CustomUserAdmin)
