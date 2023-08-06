from rest_framework import permissions


class EmailIsNotConfirmed(permissions.BasePermission):
    """
    Пользователь, чей аккаунт уже подтвержден, не имеет доступа.
    """
    def has_permission(self, request, view):
        return not request.user.email_confirmed
