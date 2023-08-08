from django.http import HttpResponseForbidden


class ActiveUserMiddleware:

    """
    Проверка аутентифицированных пользователей. Если доступ к сайту
    выполняет забаненый пользователь, возбуждается исключение 403.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_banned:
            return HttpResponseForbidden("Access Forbidden. "
                                         "\nYou are restricted from visiting the site.")  # Возвращает ошибку 403

        response = self.get_response(request)
        return response
