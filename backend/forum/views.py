from datetime import timedelta

from django.db.models import Count, ExpressionWrapper, F, IntegerField
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from accounts.models import NewUser
from accounts.serializers import DummySerializer
from forum.helpers import UpdateDestroyRetrieveMixin
from forum.logic import (
                         vote_answer_solving,)
from forum.models import (AnswerComment, Question, QuestionAnswer, QuestionAnswerImages, QuestionImages)
from forum.permissions import IsQuestionOwner
from forum.querysets import QuestionQS, QuestionAnswerQSBase, CommentQSBase
from forum.serializers import (AnswerSerializer, AskQuestionSerializer,
                               BaseQuestionSerializer, CommentSerializer,
                               DetailQuestionSerializer,
                               ListQuestionSerializer,
                               TagFieldWithCountSerializer,
                               UpdateCommentSerializer,
                               UpdateQuestionSerializer)
from forum.services import QuestionService, AnswerService, CommentService, LikeDislikeService


class AskQuestionAPIView(GenericAPIView):
    serializer_classes = {
        'POST': AskQuestionSerializer, 'GET': TagFieldWithCountSerializer
    }
    serializer_class = BaseQuestionSerializer

    permission_classes = [IsAuthenticated, ]
    queryset = QuestionQS.get_obj_list(Question)
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

        if not tag:
            raise ValidationError('Тег не указан.')

        suggested_tags = QuestionService.tag_repository.get_tags(tag)
        if not suggested_tags:
            raise ValidationError('Тег не указан')

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

        question = QuestionService.create_question(
            user=request.user, title=title, tags=tags, images=images, content=content
        )

        serializer = BaseQuestionSerializer(instance=question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)


class UpdateQuestionAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление, удаление, получение комментария.
    """
    queryset = QuestionQS.get_obj_list(Question)
    serializer_class = UpdateQuestionSerializer


class AnswerQuestionAPIView(CreateAPIView):
    """
    Оставить ответ на вопрос. Возвращается сообщение о результатах вопроса.
    """
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = serializer.validated_data.get('uploaded_images')
        question = serializer.validated_data.get('question')
        content = serializer.validated_data.get('answer')
        user = request.user

        answer = AnswerService.create_answer(
            question=question, user=user if isinstance(user, NewUser) else None, answer=content, images=images
        )

        serializer = self.serializer_class(instance=answer, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UpdateQuestionAnswerAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление, удаление, получение ответа на вопрос. Можно обновить только текст ответа.
    """
    serializer_class = AnswerSerializer
    queryset = QuestionAnswerQSBase.get_obj_list(QuestionAnswer)


class CommentAPIView(CreateAPIView):
    """
    Комментарий к ответу. Создание.
    """
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            comment = serializer.data.get('comment')
            answer_id = serializer.data.get('question_answer')
            parent_id = serializer.data.get('parent')

            comment = CommentService.create_comment(
                comment=comment, question_answer_id=answer_id, user=request.user, parent_id=parent_id
            )

            serializer = self.serializer_class(instance=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCommentAPIView(UpdateDestroyRetrieveMixin):
    """
    Обновление комментария.
    """
    queryset = CommentQSBase.get_obj_list(AnswerComment)
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
            return Response(data='Вы не можете голосовать за свою собственную запись.',
                            status=status.HTTP_403_FORBIDDEN)

        LikeDislikeService.like(obj=instance, user=user)

        return Response(data='Лайк поставлен успешно')

    @swagger_auto_schema(manual_parameters=[model])
    @action(detail=True, methods=['get'])
    def dislike(self, request, pk=None):
        instance = self.get_object(pk)
        user = request.user

        if instance.user == user:
            return Response(data='Вы не можете голосовать за свою собственную запись.',
                            status=status.HTTP_403_FORBIDDEN)

        LikeDislikeService.dislike(obj=instance, user=user)

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
    Параметр sort - best/latest/closed/opened.
    """
    http_method_names = ('get',)
    serializer_classes = {
        'list': ListQuestionSerializer,
        'retrieve': DetailQuestionSerializer,
    }

    limit = openapi.Parameter(name='page', in_=openapi.IN_QUERY,
                              description="страница, min=0",
                              type=openapi.TYPE_STRING, required=True)

    sort = openapi.Parameter(name='sort', in_=openapi.IN_QUERY,
                             description="сортировка от большего к меньшему best/latest/closed/opened",
                             type=openapi.TYPE_STRING, required=False)

    @swagger_auto_schema(manual_parameters=[limit, sort])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_queryset(self):
        query_params = self.request.query_params
        page = query_params.get('page')
        if page:
            page = int(page)
            offset = page * 10
            limit = page * 10 + 10

        sort = query_params.get('sort')
        if not sort and ((not page and page != 0) or not self.action == 'list'):
            return Question.objects.all().order_by('-creation_date')
        elif sort == 'closed' and (page or page == 0):
            return Question.objects.filter(is_solved=True).order_by('-creation_date')[offset:limit]
        elif sort == 'opened' and (page or page == 0):
            return Question.objects.filter(is_solved=False).order_by('-creation_date')[offset:limit]
        elif sort == 'best' and (page or page == 0):

            month_ago = timezone.now() - timedelta(days=30)
            amount_of_questions = 100

            questions = Question.objects.annotate(
                answer_count=Count('question_answers'),
                comment_count=Count('question_answers__answer_comments'),
                like_count=Count('rating__users_liked'),
                dislike_count=Count('rating__users_disliked'),
                score=ExpressionWrapper(
                    F('like_count') + F('answer_count') * 2 +
                    F('comment_count') - F('dislike_count') * 0.5,
                    output_field=IntegerField()
                )
            ).filter(creation_date__gte=month_ago).order_by('-score', '-creation_date')[:amount_of_questions]
            return questions

        return Question.objects.all()[offset:limit]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class AnswerViewSet(ModelViewSet):
    """
    Возвращение списка ответов / ответ по id.
    """
    queryset = QuestionAnswer.objects.all()
    serializer_class = AnswerSerializer
    http_method_names = ('get',)


class RetrieveCommentAPIView(RetrieveAPIView):
    """
    Возвращение комментария по id.
    """
    queryset = CommentQSBase.get_obj_list(AnswerComment)
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


class ComplainAPIView(GenericAPIView):
    """
    Пожаловаться на comment, answer, question. Доступно для
    аутентифицированных пользователей. content_type=question/answer/comment/.
    """
    serializer_class = DummySerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['patch', ]

    def patch(self, request, content_type, content_id):
        obj = None
        if content_type == 'question':
            obj = Question.objects.get(id=content_id)
        elif content_type == 'answer':
            obj = QuestionAnswer.objects.get(id=content_id)
        elif content_type == 'comment':
            obj = AnswerComment.objects.get(id=content_id)
        else:
            return Response(data={'message': 'content_type не корректен'},
                            status=status.HTTP_400_BAD_REQUEST)

        obj.rating.users_complained.add(request.user)
        return Response(status=status.HTTP_200_OK)
