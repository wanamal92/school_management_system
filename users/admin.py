from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'full_name']
    ordering = ['full_name']
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'role', 'profile_image')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
