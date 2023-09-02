from rest_framework import serializers

from forum.models import AnswerComment, Question, QuestionAnswer, ThemeTag
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
        required=False, child=serializers.ImageField(allow_empty_file=False, use_url=False, write_only=True),
        validators=[validate_answer_related_obj_amount]
    )

    class Meta:
        model = QuestionAnswer
        fields = ('question', 'answer', 'uploaded_images')


class UpdateQuestionAnswerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления ответа на вопрос.
    """
    class Meta:
        model = QuestionAnswer
        fields = ('answer',)


class UpdateQuestionSerializer(serializers.ModelSerializer):
    """
    Серилизатор для обновления вопроса.
    """
    class Meta:
        model = Question
        fields = ('content', )


class CreateCommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания комментария.
    """
    class Meta:
        model = AnswerComment
        fields = ('question_answer', 'comment',)


class UpdateCommentSerializer(serializers.ModelSerializer):
    """
    Обновление комментария.
    """
    class Meta:
        model = AnswerComment
        fields = ('comment',)
