from accounts.models import NewUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from forum.helpers import UpdateDestroyRetrieveMixin
from forum.logic import (add_image, create_return_tags, get_tags_or_error,
                         vote_answer_solving)
from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerImages, QuestionImages)
from forum.permissions import IsQuestionOwner
from forum.serializers import (AnswerSerializer, AskQuestionSerializer,
                               CommentSerializer, DetailQuestionSerializer,
                               ListQuestionSerializer, TagFieldSerializer,
                               UpdateCommentSerializer,
                               UpdateQuestionSerializer)


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
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
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

        data = {
            'question': question.id,
            'title': question.title,
            'content': question.content,
            'user': str(question.user)
        }

        return Response(data=data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)


class UpdateQuestionAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление, удаление, получение комментария.
    """
    queryset = Question.objects.all()
    serializer_class = UpdateQuestionSerializer


class AnswerQuestionAPIView(CreateAPIView):
    """
    Оставить ответ на вопрос. Возвращается сообщение о результатах вопроса.
    """
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = serializer.data.get('uploaded_images')
        question = serializer.data.get('question')
        answer = serializer.data.get('answer')
        user = request.user
        question_answer = QuestionAnswer.objects.create(
            question_id=question,
            answer=answer,
        )
        if isinstance(user, NewUser):
            question_answer.user = request.user
            question_answer.save()

        if images:
            add_image(images=images, obj_model=question_answer, attachment_model=QuestionAnswerImages)

        serializer = self.serializer_class(instance=question_answer, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UpdateQuestionAnswerAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление, удаление, получение ответа на вопрос. Можно обновить только текст ответа.
    """
    serializer_class = AnswerSerializer
    queryset = QuestionAnswer.objects.all()


class CommentAPIView(CreateAPIView):
    """
    Комментарий к ответу. Создание.
    """
    serializer_class = CommentSerializer


class UpdateCommentAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление комментария.
    """
    queryset = AnswerComment.objects.all()
    serializer_class = UpdateCommentSerializer


class LikeDislikeViewSet(GenericViewSet):
    """
    Лайк/Дизлайк экземпляра модели. Требуется query_param, представляющий собой модель.
    Он представляет собой экземпляр класса модели Вопроса (question) или ответа (answer).
    Пример:

    example.com/api/v1/forum/likes/{id}/dislike/?model=question
    ставит дизлайк экземпляру модели Вопроса.
    """
    permission_classes = [IsAuthenticated]
    model = openapi.Parameter(name='model', in_=openapi.IN_QUERY,
                              description="Модель/сущность, e.g. question, answer",
                              type=openapi.TYPE_STRING, required=True)

    @swagger_auto_schema(manual_parameters=[model])
    @action(detail=True, methods=['get'])
    def like(self, request, pk=None):
        instance = self.get_object(pk)
        user = request.user

        if instance.user == user:
            return Response(data='Вы не можете голосовать за свою собственную запись.', status=status.HTTP_403_FORBIDDEN)
        instance.like(user=user)

        return Response(data='Лайк поставлен успешно')

    @swagger_auto_schema(manual_parameters=[model])
    @action(detail=True, methods=['get'])
    def dislike(self, request, pk=None):
        instance = self.get_object(pk)
        user = request.user

        if instance.user == user:
            return Response(data='Вы не можете голосовать за свою собственную запись.', status=status.HTTP_403_FORBIDDEN)
        instance.dislike(user=user)

        return Response(data='Дизлайк поставленен успешно')

    def get_object(self, pk):
        if 'model' in self.request.query_params:
            model_name = self.request.query_params['model']
            if model_name == 'question':
                return Question.objects.get(pk=pk)
            elif model_name == 'answer':
                return QuestionAnswer.objects.get(pk=pk)
        raise ValueError('Параметр запроса несуществует или указан неверно.')


class QuestionViewSet(ModelViewSet):
    """
    Листинг вопросов и вопроса со всеми его ответами и комментариями.
    Параметр запроса - limit, определяющий кол-во возвращаемых записей.
    """
    serializer_classes = {'list': ListQuestionSerializer, 'retrieve': DetailQuestionSerializer}
    http_method_names = ('get', )

    limit = openapi.Parameter(name='limit', in_=openapi.IN_QUERY,
                              description="кол-во возвращаемых записей",
                              type=openapi.TYPE_STRING, required=True)

    @swagger_auto_schema(manual_parameters=[limit])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_queryset(self):
        limit = self.request.query_params.get('limit')
        queryset = Question.objects.all()[:limit]
        return queryset


class AnswerViewSet(ModelViewSet):
    """
    Возвращение списка ответов / ответ по id.
    """
    queryset = QuestionAnswer.objects.all()
    serializer_class = AnswerSerializer
    http_method_names = ('get', )


class RetrieveCommentAPIView(RetrieveAPIView):
    """
    Возвращение комментария по id.
    """
    queryset = AnswerComment.objects.all()
    serializer_class = CommentSerializer


class MarkAnswerSolving(RetrieveAPIView):
    """
    Отмечает ответ на вопрос, как решающий проблему.
    """
    queryset = QuestionAnswer.objects.all()
    permission_classes = [IsAuthenticated, IsQuestionOwner]
    serializer_class = None

    def get(self, request, *args, **kwargs):
        answer = self.get_object()
        related_question = answer.question

        vote_answer_solving(answer=answer, related_question=related_question)

        return Response(status=status.HTTP_200_OK)
