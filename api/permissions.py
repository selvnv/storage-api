from rest_framework import permissions
from rest_framework.response import Response

from api.models import UserRole


class ProviderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Доступ на выполнение безопасных методов - для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для всех остальных методов доступ только для авторизованных пользователей с ролью provider
        if not request.user.is_authenticated:
            return False

        user_roles = request.user.roles.all()
        if 'provider' not in [role.name for role in user_roles]:
            return False
        return True

class ConsumerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Доступ на выполнение безопасных методов - для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для всех остальных методов доступ только для авторизованных пользователей с ролью consumer
        if not request.user.is_authenticated:
            return False

        user_roles = request.user.roles.all()
        if 'consumer' not in [role.name for role in user_roles]:
            return False
        return True
