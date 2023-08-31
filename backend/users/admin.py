from django.contrib import admin

from .models import CustomGroup, CustomUser, Group


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'date_joined',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.unregister(Group)


@admin.register(CustomGroup)
class CustomGroup(admin.ModelAdmin):
    ...
