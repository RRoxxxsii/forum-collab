from rest_framework import serializers

from notifications.models import Notification


class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
        extra_kwargs = {'target_content_type': {'required': False}}


class NotificationListIDSerializer(serializers.Serializer):
    list_id = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        fields = ('__all__', )
