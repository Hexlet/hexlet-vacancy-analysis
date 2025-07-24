from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UAdmin

from .models import User


@admin.register(User)
class UserAdmin(UAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    ordering = ('email',)
    search_fields = ('email',)

    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')}
        ),
        (
            'Permissions',
            {
                'fields':
                (
                    'is_staff',
                    'is_active',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (
            'Important dates',
            {'fields': ('last_login',)}
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields':
                (
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                )
            }
        ),
    )
