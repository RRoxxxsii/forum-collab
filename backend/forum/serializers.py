from __future__ import annotations

from accounts.serializers import UserSerializer
from rest_framework import serializers

from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerRating, QuestionRating, ThemeTag)
from forum.validators import (validate_answer_related_obj_amount,
                              validate_question_related_obj_amount,
                              validate_tags_amount)


class BaseTagFieldSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('tag_name', 'is_relevant', 'is_user_tag')
        model = ThemeTag


class TagFieldWithCountSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегов для GET-запроса с числом использования тегов.
    """
    use_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('tag_name', 'use_count', 'is_relevant', 'is_user_tag')
        model = ThemeTag

    def get_use_count(self, instance: ThemeTag):
        return instance.questions.all().count()


class AskQuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания вопроса.
    """
    tags = serializers.ListField(required=True, validators=[validate_tags_amount],
                                 allow_empty=False)
    uploaded_images = serializers.ListField(
        required=False, child=serializers.ImageField(allow_empty_file=False, use_url=False, write_only=True),
        validators=[validate_question_related_obj_amount]
    )

    class Meta:
        model = Question
        fields = ('tags', 'title', 'content', 'uploaded_images')


class UpdateQuestionSerializer(serializers.ModelSerializer):
    """
    Серилизатор для обновления вопроса.
    """
    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'creation_date', 'updated_date')
        extra_kwargs = {'title': {'required': False}}


class UpdateCommentSerializer(serializers.ModelSerializer):
    """
    Обновление комментария.
    """
    class Meta:
        model = AnswerComment
        fields = ('id', 'user',  'comment', 'question_answer', 'creation_date', 'updated_date')
        read_only_fields = ('id', 'question_answer', 'creation_date', 'updated_date', 'user')


class BaseRatingIsLikedOrDislikedSerializer(serializers.Serializer):
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'

    def get_is_liked(self, instance: [Question | QuestionAnswer]) -> bool:
        user = self.context.get('request').user
        return instance.users_liked.filter(id=user.id).exists()

    def get_is_disliked(self, instance:  [Question | QuestionAnswer]) -> bool:
        user = self.context.get('request').user
        return instance.users_disliked.filter(id=user.id).exists()


class QuestionRatingSerializer(BaseRatingIsLikedOrDislikedSerializer, serializers.ModelSerializer):

    class Meta:
        model = QuestionRating
        fields = '__all__'


class AnswerRatingSerializer(BaseRatingIsLikedOrDislikedSerializer, serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswerRating
        fields = '__all__'
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"},
                        'updated_date': {'format': "%Y-%m-%d %H:%M:%S"}}


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AnswerComment
        fields = '__all__'
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"},
                        'updated_date': {'format': "%Y-%m-%d %H:%M:%S"}}
        read_only_fields = ('creation_date', 'updated_date', 'user')


class AnswerSerializer(serializers.ModelSerializer):
    rating = AnswerRatingSerializer(read_only=True)
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='answer-detail',
                                                 source='answer_images')
    comments = CommentSerializer(read_only=True, many=True, source='answer_comments')

    uploaded_images = serializers.ListField(
        required=False, child=serializers.ImageField(allow_empty_file=False, use_url=False),
        validators=[validate_answer_related_obj_amount]
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'question', 'user', 'answer', 'is_solving', 'creation_date', 'updated_date',
                  'rating', 'images', 'comments', 'uploaded_images')
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"},
                        'updated_date': {'format': "%Y-%m-%d %H:%M:%S"}}
        read_only_fields = ('id', 'user', 'is_solving', 'creation_date', 'updated_date', 'rating',
                            'images', 'comments')


class QuestionRelatedAnswersAmountSerializer(serializers.Serializer):
    answers_amount = serializers.SerializerMethodField()

    def get_answers_amount(self, instance: Question):
        return instance.question_answers.all().count()


class ListQuestionSerializer(QuestionRelatedAnswersAmountSerializer, serializers.ModelSerializer):
    rating = QuestionRatingSerializer(read_only=True)
    tags = BaseTagFieldSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'answers_amount', 'is_solved',
                  'creation_date', 'updated_date', 'rating', 'tags')
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"},
                        'updated_date': {'format': "%Y-%m-%d %H:%M:%S"}}


class DetailQuestionSerializer(QuestionRelatedAnswersAmountSerializer, serializers.ModelSerializer):

    rating = QuestionRatingSerializer(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True, source='question_answers')
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='question-detail',
                                                 source='question_images')
    tags = BaseTagFieldSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'answers_amount', 'is_solved', 'creation_date', 'updated_date',
                  'images', 'rating', 'answers', 'tags')
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"},
                        'updated_date': {'format': "%Y-%m-%d %H:%M:%S"}}


class GenericObjNotificationRelatedField(serializers.RelatedField):
    """
    Возвращает сериализованные данные объекта в зависимости от типа.
    """
    def to_representation(self, value: [Question | AnswerComment | QuestionAnswer]):
        if isinstance(value, Question):
            serializer = ListQuestionSerializer(value)
        if isinstance(value, AnswerComment):
            serializer = CommentSerializer(value)
        if isinstance(value, QuestionAnswer):
            serializer = AnswerSerializer(value)
        return serializer.data


# class UserNotificationListSerializer(serializers.ModelSerializer):
#     recipient = UserSerializer(read_only=True)
#     actor = UserSerializer(read_only=True)
#     target = GenericObjNotificationRelatedField(read_only=True)
#     action_object = GenericObjNotificationRelatedField(read_only=True)
#     type = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Notification
#         fields = ('type', 'id', 'recipient', 'actor', 'verb', 'unread',
#                   'target', 'action_object', 'timestamp')
#
#     def get_type(self, value):
#         if isinstance(value.target, Question):
#             return 'Question'
#         elif isinstance(value.target, AnswerComment):
#             return 'Comment'
#         elif isinstance(value.target, QuestionAnswer):
#             return 'Answer'
