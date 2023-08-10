from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import EmailConfirmationToken


class BaseEmailConfirmAPIView(APIView):
    """
    Базовый класс для подтверждения email и связанных действий.
    """
    success_message = None  # Переопределять в дочерних классах
    error_message = None    # Переопределять в дочерних классах

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
