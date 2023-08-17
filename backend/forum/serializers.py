from rest_framework import serializers

from forum.models import Question
from forum.validators import validate_tags


class AskQuestionSerializer(serializers.ModelSerializer):
    tag_ids = serializers.ListField(required=True, validators=[validate_tags, ])

    class Meta:
        model = Question
        fields = ('tag_ids', 'author', 'title', 'content')


class TagFieldSerializer(serializers.Serializer):
    tags = serializers.ListField()

    class Meta:
        fields = ('tags',)


