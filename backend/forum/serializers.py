from rest_framework import serializers

from forum.models import Question, ThemeTag
from forum.validators import validate_tags_amount, validate_tags_exist


class AskQuestionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(required=True, validators=[validate_tags_amount, validate_tags_exist],
                                 allow_empty=False)

    class Meta:
        model = Question
        fields = ('tags', 'author', 'title', 'content')


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
