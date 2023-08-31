from django.contrib import admin

from .models import CustomGroup, CustomUser, Follow, Group


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
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
class CustomGroupAdmin(admin.ModelAdmin):
    ...


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'follower',
        'author',
    )
    search_fields = ('follower', 'author')
