from rest_framework import serializers

from forum.models import Question, QuestionAnswer, ThemeTag
from forum.validators import validate_related_obj_amount, validate_tags_amount


class AskQuestionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(required=True, validators=[validate_tags_amount],
                                 allow_empty=False)
    uploaded_images = serializers.ListField(
        required=False, child=serializers.ImageField(allow_empty_file=False, use_url=False, write_only=True),
        validators=[validate_related_obj_amount]
    )

    class Meta:
        model = Question
        fields = ('tags', 'title', 'content', 'uploaded_images')


class TagFieldSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегов для GET-запроса.
    """
    use_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('tag', 'use_count', 'is_relevant', 'is_user_tag')
        model = ThemeTag

    def get_use_count(self, obj: ThemeTag):
        return obj.questions.all().count()


class AnswerQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ('question', 'answer')


class UpdateQuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ('answer',)


class UpdateQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('content',)
