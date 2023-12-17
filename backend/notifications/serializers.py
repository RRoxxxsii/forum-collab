from forum.models import AnswerComment, Question, QuestionAnswer
from forum.serializers import (BaseAnswerSerializer, BaseQuestionSerializer,
                               CommentSerializer)
from notifications.models import Notification
from rest_framework import serializers


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
        if isinstance(instance.target, Question) and isinstance(instance.action_obj, QuestionAnswer):
            data.update(
                {
                    "target": BaseQuestionSerializer(instance.target).data,
                    "target_content_type": "question",
                    "action_obj": BaseAnswerSerializer(instance.action_obj).data,
                    "action_obj_content_type": "answer"
                }
            )
        elif isinstance(instance.target, QuestionAnswer) and isinstance(instance.action_obj, AnswerComment):
            data.update(
                {
                    "question": BaseQuestionSerializer(instance.target.question).data,
                    "target": BaseAnswerSerializer(instance.target).data,
                    "target_content_type": "answer",
                    "comment": CommentSerializer(instance.action_obj).data,
                    "action_obj_content_type": "comment"
                }
            )
        elif isinstance(instance.target, AnswerComment) and instance(instance.action_obj, AnswerComment):
            data.update(
                {
                    "question": BaseQuestionSerializer(instance.target.question_answer.question.data),
                    "target": CommentSerializer(instance.target).data,
                    "target_content_type": "comment",
                    "action_obj": CommentSerializer(instance.action_obj).data,
                    "action_obj_content_type": "comment"
                }
            )
        return data


class NotificationListIDSerializer(serializers.Serializer):
    list_id = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        fields = ('__all__', )
