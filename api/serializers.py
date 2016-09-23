from abc import ABCMeta
from rest_framework import serializers
from api.models import *


class BaseSerializer(metaclass=ABCMeta):
    class Meta(metaclass=ABCMeta):
        depth = 1
        fields = '__all__'


class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'role',
            'department',
            'level',
            'balance',
            'rating',
            'phone',
            'avatar',
            'tasks',
            'achievements',
        )


class LevelSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Level


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class TaskSerializer(BaseSerializer):
    progress = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    def get_progress(self, obj):
        pass

    def get_user_progress(self, obj):
        pass

    class Meta(BaseSerializer.Meta):
        model = Task
        fields = ('id', 'name', 'desc', 'type', 'total_count', 'requests')


class RequestSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Request


class AchievementSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Achievement
        fields = ('name', 'desc', 'pic', 'users', 'tasks')


class AttachmentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Attachment


class BalanceLogSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = BalanceLog
