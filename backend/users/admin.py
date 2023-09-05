from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import Subscribe, User


class UserResource(ModelResource):
    """Модель ресурсов пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'date_joined',
        )


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    """
    Регистрация модели пользователей
    и импорта/эскпорта в админ-панели.
    """

    resource_class = (UserResource,)
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


class SubscribeResource(ModelResource):
    """Модель ресурсов подписок."""

    class Meta:
        model = Subscribe
        fields = (
            'id',
            'user',
            'author',
        )


@admin.register(Subscribe)
class SubscribeAdmin(ImportExportModelAdmin):
    """Регистрация модели подписок и импорта/эскпорта в админ-панели."""

    resource_class = (SubscribeResource,)
    list_display = (
        'id',
        'user',
        'author',
    )
    list_filter = (
        'author',
        'user',
    )
    search_fields = [
        'user__username',
        'user__username',
        'user__first_name',
        'user__last_name',
    ]
