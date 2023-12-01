from __future__ import annotations

from rest_framework import serializers

from accounts.serializers import UserSerializer
from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerRating, QuestionRating, ThemeTag)
from forum.validators import (validate_answer_related_obj_amount,
                              validate_question_related_obj_amount,
                              validate_tags_amount)


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    image = serializers.SerializerMethodField()
    alt_text = serializers.CharField(max_length=255)

    class Meta:
        fields = '__all__'

    def get_image(self, instance):
        request = self.context.get('request')
        image_url = instance.image.url
        return request.build_absolute_uri(image_url)


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
        fields = ('id', 'tag_name', 'use_count', 'is_relevant', 'is_user_tag')
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
        required=False, child=serializers.ImageField(allow_empty_file=False, use_url=False),
        validators=[validate_question_related_obj_amount]
    )

    class Meta:
        model = Question
        fields = ('tags', 'title', 'content', 'uploaded_images')


class UpdateQuestionSerializer(serializers.ModelSerializer):
    """
    Серилизатор для обновления вопроса.
    """
    tags = TagFieldWithCountSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'creation_date', 'updated_date', 'tags')
        extra_kwargs = {'title': {'required': False}}


class UpdateCommentSerializer(serializers.ModelSerializer):
    """
    Обновление комментария.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = AnswerComment
        fields = ('id', 'user',  'comment', 'question_answer', 'parent', 'creation_date', 'updated_date')
        read_only_fields = ('id', 'question_answer', 'creation_date', 'parent', 'updated_date', 'user')


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
        exclude = ('users_complained', )


class AnswerRatingSerializer(BaseRatingIsLikedOrDislikedSerializer, serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswerRating
        exclude = ('users_complained', )
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
    images = serializers.SerializerMethodField()
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

    def get_images(self, instance):
        serializer_context = {'request': self.context.get('request')}
        qs = instance.answer_images.all()
        serializer = ImageSerializer(qs, many=True, context=serializer_context)
        return serializer.data


class QuestionRelatedAnswersAmountSerializer(serializers.Serializer):
    answers_amount = serializers.SerializerMethodField()

    def get_answers_amount(self, instance: Question):
        return instance.question_answers.all().count()


class BaseQuestionSerializer(serializers.ModelSerializer):
    tags = BaseTagFieldSerializer(read_only=True, many=True)
    user = serializers.SerializerMethodField(read_only=True)
    question = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Question
        fields = ('question', 'title', 'content', 'user', 'tags')

    def get_user(self, instance):
        return instance.user.user_name


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
    images = serializers.SerializerMethodField()
    tags = BaseTagFieldSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'answers_amount', 'is_solved', 'creation_date', 'updated_date',
                  'images', 'rating', 'answers', 'tags')
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"},
                        'updated_date': {'format': "%Y-%m-%d %H:%M:%S"}}

    def get_images(self, instance):
        serializer_context = {'request': self.context.get('request')}
        qs = instance.question_images.all()
        serializer = ImageSerializer(qs, many=True, context=serializer_context)
        return serializer.data


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
