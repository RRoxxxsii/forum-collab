from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from forum.helpers import UpdateDestroyRetrieveMixin
from forum.logic import add_image, create_return_tags, get_tags_or_error
from forum.models import Question, QuestionAnswer, QuestionAnswerImages, QuestionImages, AnswerComment
from forum.serializers import (AnswerQuestionSerializer, AskQuestionSerializer,
                               TagFieldSerializer,
                               UpdateQuestionAnswerSerializer,
                               UpdateQuestionSerializer, CreateCommentSerializer, UpdateCommentSerializer)


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
        images = serializer.data.get('uploaded_images')
        question = Question.objects.create(
            user=request.user,
            title=title,
            content=content
        )

        if images:
            add_image(images=images, obj_model=question, attachment_model=QuestionImages)

        tag_ids = create_return_tags(tags=tags, user=request.user)
        question.tags.add(*tag_ids)
        question.save()

        return Response(data=self.success_message, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)


class UpdateQuestionAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление, удаление, получение комментария.
    """
    queryset = Question.objects.all()
    serializer_class = UpdateQuestionSerializer


class AnswerQuestionAPIView(GenericAPIView):
    """
    Оставить ответ на вопрос. Возвращается сообщение о результатах вопроса.
    """
    serializer_class = AnswerQuestionSerializer
    permission_classes = [IsAuthenticated, ]
    success_message = 'Ответ на вопрос успешно опубликован.'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = serializer.data.get('uploaded_images')
        question = serializer.data.get('question')
        answer = serializer.data.get('answer')
        question_answer = QuestionAnswer.objects.create(
            question_id=question,
            answer=answer,
            user=request.user
        )
        if images:
            add_image(images=images, obj_model=question_answer, attachment_model=QuestionAnswerImages)
        return Response(data=self.success_message, status=status.HTTP_201_CREATED)


class UpdateQuestionAnswerAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление, удаление, получение ответа на вопрос. Можно обновить только текст ответа.
    """
    serializer_class = UpdateQuestionAnswerSerializer
    queryset = QuestionAnswer.objects.all()


class CommentAPIView(CreateAPIView):
    """
    Комментарий к ответу. Создание.
    """
    serializer_class = CreateCommentSerializer


class UpdateCommentAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление комментария.
    """
    queryset = AnswerComment.objects.all()
    serializer_class = UpdateCommentSerializer
