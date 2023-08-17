from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from forum.models import Question, ThemeTag
from forum.serializers import AskQuestionSerializer, TagFieldSerializer


class AskQuestionAPIView(GenericAPIView):
    serializer_classes = {'POST': AskQuestionSerializer, 'GET': TagFieldSerializer}
    permission_classes = [IsAuthenticated, ]
    queryset = Question.objects.all()
    success_message = 'Вопрос успешно опубликован.'
    q = openapi.Parameter(name='q', in_=openapi.IN_QUERY,
                          description="Ввод символов для поиска совпадений по тегам",
                          type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[q])
    def get(self, request, *args, **kwargs):
        """
        Возвращается список тегов.
        """

        # Сделать сортировку по количеству запросов
        raise NotImplementedError
        tag = request.query_params.get('q')
        suggested_tags = ThemeTag.objects.filter(tag__icontains=tag).values_list('tag', flat=True)
        print(suggested_tags)
        serializer = self.get_serializer_class()(data=suggested_tags, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Создание вопроса. Поле user заполняется автоматически.
        Возвращает сообщение о результатах запроса.
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.data.get('title')
        content = serializer.data.get('content')
        tag_ids = serializer.data.get('tag_ids')
        question = Question.objects.create(
            author=request.user,
            title=title,
            content=content
        )
        question.tags.add(*tag_ids)
        return Response(data=self.success_message, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)


class LeaveAnswerAPIView(GenericAPIView):
    """
    Оставить ответ на вопрос. Возвращается сообщение о результатах вопроса.
    """
    pass

