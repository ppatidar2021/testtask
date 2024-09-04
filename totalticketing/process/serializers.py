from rest_framework import serializers

from .models import UserTask


class UserTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTask
        fields = ["user", "task_id", "is_completed"]
