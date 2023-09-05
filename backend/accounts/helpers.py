from dataclasses import dataclass

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from accounts.models import EmailConfirmationToken
from accounts.serializers import DummySerializer


@dataclass(init=False, repr=False, eq=False)
class BaseEmailConfirmMixin:
    """
    Базовый класс для подтверждения email и связанных действий.
    """
    success_message: str = ''    # Переопределять в дочерних классах
    error_message: str = ''      # Переопределять в дочерних классах

    def perform_action(self, user):
        raise NotImplementedError("Метод perform_action должен быть переопределен в дочерних классах.")


class BaseEmailConfirmAPIView(BaseEmailConfirmMixin, GenericAPIView):

    def get(self, request):
        token_id = request.GET.get('token_id', None)
        user_id = request.GET.get('user_id', None)
        try:
            token = EmailConfirmationToken.objects.get(id=token_id, user=user_id)
            user = token.user
            self.perform_action(user)
            return Response(data=self.success_message, status=200)
        except EmailConfirmationToken.DoesNotExist:
            return Response(data=self.error_message, status=400)

    def get_serializer_class(self):
        # Возвращает сериализатор-заглушку, так как представление класса не нуждается в сериализаторе
        return DummySerializer
