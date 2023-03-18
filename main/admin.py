from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    search_fields = ('email', 'first_name', 'last_name', )
    ordering = ('-created_on', )
    list_filter = ('email', 'first_name', 'last_name',  'is_active', 'is_staff', )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', )

    fieldsets = (
        ('Personal', {'fields': ('email', 'first_name', 'last_name', 'password', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'first_name', 'last_name','password1', 'password2', 'is_active', 'is_staff', 'is_superuser', ),
        }),
    )


admin.site.register(User, CustomUserAdmin)