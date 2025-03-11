from rest_framework import permissions

ADMIN_USER_ROLE = "admin"
PROVIDER_USER_ROLE = "provider"
CONSUMER_USER_ROLE = "consumer"


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class AdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        if request.user.is_authenticated:
            user_roles = request.user.roles.all()
            if ADMIN_USER_ROLE in [role.name for role in user_roles]:
                return True

        return False


class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or request.user.username == obj.username
        )


class ProviderOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Доступ на выполнение безопасных методов - для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для всех остальных методов доступ только для авторизованных
        # пользователей с ролью provider
        if request.user.is_authenticated:
            user_roles = request.user.roles.all()
            if PROVIDER_USER_ROLE in [role.name for role in user_roles]:
                return True

        return False


class ConsumerOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Доступ на выполнение безопасных методов - для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для всех остальных методов доступ только для авторизованных
        # пользователей с ролью consumer
        if request.user.is_authenticated:
            user_roles = request.user.roles.all()
            if CONSUMER_USER_ROLE in [role.name for role in user_roles]:
                return True

        return False
