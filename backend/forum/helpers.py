from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (DestroyModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from forum.permissions import IsOwner


class UpdateDestroyRetrieveMixin(GenericAPIView, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    """
    Миксин для обновления, удаления и получения.
    """
    permission_classes = [IsOwner, IsAuthenticatedOrReadOnly]
    allowed_methods = ['PUT', 'DELETE', 'GET']

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
