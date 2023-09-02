from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    """
    Только автор записи имеет право редактировать.
    """
    message = 'Редактировать запись может только автор.'

    def has_object_permission(self, request, view, instance):
        if request.method in SAFE_METHODS:
            return True

        return instance.user == request.user
