from rest_framework import serializers
from api.models import UserRole


class FilteredRoles(serializers.PrimaryKeyRelatedField):
    """
    Динамическое изменение ролей пользователя в зависимости от прав доступа
    """

    def get_queryset(self):
        request = self.context.get("request")

        if request is not None:
            if request.user and request.user.is_authenticated:
                # Учитываются как внутренние роли, так и роль django-админа
                if request.user.roles.filter(name="admin").exists() or request.user.is_staff:
                    return UserRole.objects.all()  # Админ видит все роли

        return UserRole.objects.exclude(is_service=True)  # Остальные не видят служебные роли
