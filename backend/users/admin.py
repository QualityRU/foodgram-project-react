from django.contrib import admin

from .models import CustomGroup, CustomUser, Group


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    ...


admin.site.unregister(Group)


@admin.register(CustomGroup)
class CustomGroup(admin.ModelAdmin):
    ...
