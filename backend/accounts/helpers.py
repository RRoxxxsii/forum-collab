from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from accounts.models import EmailConfirmationToken
from accounts.serializers import DummySerializer


class BaseEmailConfirmAPIView(GenericAPIView):
    """
    Базовый класс для подтверждения email и связанных действий.
    """
    success_message = None  # Переопределять в дочерних классах
    error_message = None    # Переопределять в дочерних классах

    def get_serializer_class(self):
        # Возвращает сериализатор-заглушку, так как представление класса не нуждается в сериализаторе
        return DummySerializer

    def perform_action(self, user):
        raise NotImplementedError("Метод perform_action должен быть переопределен в дочерних классах.")

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
