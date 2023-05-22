from rest_framework import permissions


class OnlyAdmin(permissions.BasePermission):
    """Разрешение изменений и просмотр только администратору."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.admin or request.user.is_superuser
        return False


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешение изменения только автору, администратору
    и модератору или доступен просмотр всем пользователям.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.moderator
                or request.user.admin)


class ReadOnly(permissions.BasePermission):
    """
    Предоставление прав просмотра записи любой
    категорией пользователей.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
