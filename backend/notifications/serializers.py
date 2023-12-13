from rest_framework import serializers

from forum.models import Question, QuestionAnswer, AnswerComment, ThemeTag
from forum.serializers import BaseQuestionSerializer, BaseTagFieldSerializer, AnswerSerializer, CommentSerializer

from notifications.models import Notification


class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            'id', 'sender', 'receiver', 'level', 'target',
            'target_object_id', 'target_content_type', 'action_obj',
            'action_obj_object_id', 'action_obj_content_type',
            'text', 'emailed', 'unread', 'creation_date'
        )
        extra_kwargs = {'target_content_type': {'required': False}}

    def to_representation(self, instance):
        data = super(NotificationsSerializer, self).to_representation(instance)
        if isinstance(instance.target, ThemeTag):
            data.update({'target': 'tag'})
        elif isinstance(instance.target, Question):
            data.update({'target': 'question'})
        elif isinstance(instance.target, QuestionAnswer):
            data.update({'target': 'answer'})
        elif isinstance(instance.target, AnswerComment):
            data.update({'target': 'comment'})
        if isinstance(instance.action_obj, ThemeTag):
            data.update({'action_obj': 'tag'})
        elif isinstance(instance.action_obj, Question):
            data.update({'action_obj': 'question'})
        elif isinstance(instance.action_obj, QuestionAnswer):
            data.update({'action_obj': 'answer'})
        elif isinstance(instance.action_obj, AnswerComment):
            data.update({'action_obj': 'comment'})
        return data


class NotificationListIDSerializer(serializers.Serializer):
    list_id = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        fields = ('__all__', )
