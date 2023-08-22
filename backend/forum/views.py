from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from forum.logic import create_return_tags, get_tags_or_error
from forum.models import Question, ThemeTag
from forum.permissions import IsOwner
from forum.serializers import AskQuestionSerializer, TagFieldSerializer, AnswerQuestionSerializer, \
    UpdateQuestionSerializer


class AskQuestionAPIView(GenericAPIView):
    serializer_classes = {'POST': AskQuestionSerializer, 'GET': TagFieldSerializer}
    permission_classes = [IsAuthenticated, ]
    queryset = Question.objects.all()
    success_message = 'Вопрос успешно опубликован.'
    q = openapi.Parameter(name='q', in_=openapi.IN_QUERY,
                          description="Ввод символов для поиска совпадений по тегам",
                          type=openapi.TYPE_STRING, required=True)

    @swagger_auto_schema(manual_parameters=[q])
    def get(self, request, *args, **kwargs):
        """
        Возвращается список тегов, количество использований, автор тега (если есть), релевантность.
        Отстортировано по статусу релевантности.
        """
        tag = request.query_params.get('q')

        suggested_tags = get_tags_or_error(tag)

        serializer = self.get_serializer_class()(suggested_tags, many=True)
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
        tags = serializer.data.get('tags')
        question = Question.objects.create(
            user=request.user,
            title=title,
            content=content
        )
        tag_ids = create_return_tags(tags=tags, user=request.user)
        question.tags.add(*tag_ids)
        question.save()

        return Response(data=self.success_message, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)


class AnswerQuestionAPIView(CreateAPIView):
    """
    Оставить ответ на вопрос. Возвращается сообщение о результатах вопроса.
    """
    serializer_class = AnswerQuestionSerializer
    permission_classes = [IsAuthenticated, ]


class UpdateAnswerAPIView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    """
    Обновление и удаление ответа на вопрос. Можно обновить только текст ответа.
    """
    serializer_class = UpdateQuestionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

