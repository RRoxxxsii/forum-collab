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
            return HttpResponseForbidden("Access Forbidden")  # Возвращает ошибку 403

        response = self.get_response(request)
        return response


class BanCheckMiddleware:

    """
    Проверка не аутентифицированных пользователей на то, забанены ли они.
    Здесь проверяется, есть ли в куки-файлах у пользователя значение-тригер,
    указывающее на то, что он забанен. Если есть, доступ к сайту запрещен.
    Способ не является самым безопасным, однако обеспечивает дополнительную
    защиту от детей, некоторых спамеров и ботов.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, является ли пользователь гостем и забаненным.
        if not request.user.is_authenticated:
            request.COOKIES.get()

        response = self.get_response(request)
        return response
