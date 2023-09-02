from rest_framework import serializers

from forum.models import AnswerComment, Question, QuestionAnswer, ThemeTag, QuestionRating, QuestionAnswerRating
from forum.validators import (validate_answer_related_obj_amount,
                              validate_question_related_obj_amount,
                              validate_tags_amount)


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


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    user_name = serializers.StringRelatedField(read_only=True, many=False, source='user')

    class Meta:
        model = Question
        fields = ('id', 'tags', 'user_id', 'user_name', 'title', 'content', 'images', 'creation_date')

    def get_tags(self, instance):
        return [tag.tag_name for tag in instance.tags.all()]

    def get_images(self, instance):
        return [image.image.url for image in instance.question_images.all()]


class TagFieldSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегов для GET-запроса.
    """
    use_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('tag_name', 'use_count', 'is_relevant', 'is_user_tag')
        model = ThemeTag

    def get_use_count(self, obj: ThemeTag):
        return obj.questions.all().count()


class AnswerQuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ответа на вопрос.
    """
    uploaded_images = serializers.ListField(
        required=False, child=serializers.ImageField(allow_empty_file=False, use_url=False),
        validators=[validate_answer_related_obj_amount]
    )

    class Meta:
        model = QuestionAnswer
        fields = ('question', 'answer', 'uploaded_images')


class RetrieveAnswerSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'question', 'user', 'answer', 'is_solving', 'images', 'creation_date')

    def get_images(self, instance):
        return [image.image.url for image in instance.answer_images.all()]


class UpdateQuestionAnswerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления ответа на вопрос.
    """
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'question', 'user', 'answer', 'creation_date', 'is_solving', 'images')
        read_only_fields = ('question', 'creation_date', 'is_solving', 'user')

    def get_images(self, instance):
        return [image.image.url for image in instance.answer_images.all()]


class UpdateQuestionSerializer(RetrieveQuestionSerializer):
    """
    Серилизатор для обновления вопроса.
    """
    class Meta:
        model = RetrieveQuestionSerializer.Meta.model
        fields = RetrieveQuestionSerializer.Meta.fields
        extra_kwargs = {'title': {'required': False}}


class CreateCommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания комментария.
    """
    class Meta:
        model = AnswerComment
        fields = ('id', 'user', 'question_answer', 'comment', 'creation_date')
        read_only_fields = ('id', 'creation_date', 'user')


class UpdateCommentSerializer(serializers.ModelSerializer):
    """
    Обновление комментария.
    """
    class Meta:
        model = AnswerComment
        fields = ('id', 'user',  'comment', 'question_answer', 'creation_date')
        read_only_fields = ('id', 'question_answer', 'creation_date', 'user')


class QuestionRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionRating
        fields = '__all__'


class AnswerRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswerRating
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerComment
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    rating = AnswerRatingSerializer(read_only=True)
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='answer-detail',
                                                 source='answer_images')
    comments = CommentSerializer(read_only=True, many=True, source='answer_comments')

    class Meta:
        model = QuestionAnswer
        fields = '__all__'


class ListQuestionSerializer(serializers.ModelSerializer):
    rating = QuestionRatingSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'creation_date', 'rating')


class DetailQuestionSerializer(serializers.ModelSerializer):

    rating = QuestionRatingSerializer(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True, source='question_answers')
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='question-detail',
                                                 source='question_images')

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'images', 'creation_date', 'rating', 'answers')
