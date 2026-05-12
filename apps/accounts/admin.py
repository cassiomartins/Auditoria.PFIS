from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'perfil', 'unidade', 'is_active')
    list_filter = ('perfil', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil PFIS', {'fields': ('perfil', 'unidade')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Perfil PFIS', {'fields': ('perfil', 'unidade')}),
    )
