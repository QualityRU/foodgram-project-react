from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import CustomUser, Follow


class CustomUserResource(ModelResource):
    """Модель ресурсов кастомных пользователей."""

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'date_joined',
        )


@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    """
    Регистрация модели кастомных пользователей
    и импорта/эскпорта в админ-панели.
    """

    resource_class = (CustomUserResource,)
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'date_joined',
    )
    list_filter = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')


class FollowResource(ModelResource):
    """Модель ресурсов подписок."""

    class Meta:
        model = Follow
        fields = (
            'id',
            'follower',
            'author',
        )


@admin.register(Follow)
class FollowAdmin(ImportExportModelAdmin):
    """Регистрация модели подписок и импорта/эскпорта в админ-панели."""

    resource_class = (FollowResource,)
    list_display = (
        'id',
        'follower',
        'author',
    )
    list_filter = (
        'author',
        'follower',
    )
    search_fields = [
        'user__username',
        'user__username',
        'user__first_name',
        'user__last_name',
    ]
