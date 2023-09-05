from rest_framework import serializers

from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerRating, QuestionRating, ThemeTag)
from forum.validators import (validate_answer_related_obj_amount,
                              validate_question_related_obj_amount,
                              validate_tags_amount)


class TagFieldSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегов для GET-запроса.
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
        fields = ('id', 'user', 'title', 'content', 'creation_date')
        extra_kwargs = {'title': {'required': False}}


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
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"}}


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerComment
        fields = '__all__'
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"}}
        read_only_fields = ('creation_date', 'user')


class AnswerSerializer(serializers.ModelSerializer):
    rating = AnswerRatingSerializer(read_only=True)
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='answer-detail',
                                                 source='answer_images')
    comments = CommentSerializer(read_only=True, many=True, source='answer_comments')

    uploaded_images = serializers.ListField(
        required=False, child=serializers.ImageField(allow_empty_file=False, use_url=False),
        validators=[validate_answer_related_obj_amount]
    )

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'question', 'user', 'answer', 'is_solving', 'creation_date',
                  'rating', 'images', 'comments', 'uploaded_images')
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"}}
        read_only_fields = ('id', 'user', 'is_solving', 'creation_date', 'rating',
                            'images', 'comments')


class ListQuestionSerializer(serializers.ModelSerializer):
    rating = QuestionRatingSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'creation_date', 'rating')
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"}}


class DetailQuestionSerializer(serializers.ModelSerializer):

    rating = QuestionRatingSerializer(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True, source='question_answers')
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='question-detail',
                                                 source='question_images')

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'content', 'is_solved', 'creation_date', 'images', 'rating', 'answers')
        extra_kwargs = {'creation_date': {'format': "%Y-%m-%d %H:%M:%S"}}
