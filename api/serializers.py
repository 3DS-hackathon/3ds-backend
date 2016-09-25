import os.path
import datetime
from abc import ABCMeta
from rest_framework import serializers
from rest_framework import fields
from api.models import *


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(value.timestamp())

    def to_internal_value(self, data):
        return datetime.datetime.fromtimestamp(data)


class BaseSerializer(serializers.ModelSerializer):
    class Meta(metaclass=ABCMeta):
        depth = 1
        fields = '__all__'


class LevelSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Level


class AchievementSerializer(BaseSerializer):
    pic = fields.FileField(allow_empty_file=False, use_url=True)

    class Meta(BaseSerializer.Meta):
        model = Achievement
        fields = ('id', 'name', 'desc', 'pic',
                  'background_color', 'text_color')


class TaskSerializer(BaseSerializer):
    start_timestamp = TimestampField()
    end_timestamp = TimestampField()
    progress = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    achievements = AchievementSerializer(many=True)

    def get_progress(self, obj):
        try:
            user = self.context['request'].user
            return TaskStatus.objects.get(user=user, task=obj).progress
        except KeyError:
            return None
        except TaskStatus.DoesNotExist:
            return None

    def get_status(self, obj):
        try:
            user = self.context['request'].user
            return TaskStatus.objects.get(user=user, task=obj).status
        except KeyError:
            return 'pending'
        except TaskStatus.DoesNotExist:
            return 'pending'

    class Meta(BaseSerializer.Meta):
        model = Task
        fields = ('id', 'name', 'desc', 'type', 'total_count',
                  'experience', 'price', 'start_timestamp', 'status',
                  'end_timestamp', 'progress', 'achievements')


class UserSerializer(BaseSerializer):
    level = LevelSerializer(source='get_level')
    avatar = fields.FileField(read_only=True, use_url=True)
    balance = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True)
    achievements = AchievementSerializer(many=True)

    def get_balance(self, obj):
        return obj.get_balance()

    class Meta(BaseSerializer.Meta):
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'balance', 'rating',
                  'phone', 'avatar', 'tasks', 'level', 'achievements', 'department')


class DepartmentSerializer(serializers.ModelSerializer):
    avatar = fields.FileField(read_only=True, use_url=True)
    rating = serializers.SerializerMethodField()
    achievements = AchievementSerializer(many=True)
    users = UserSerializer(many=True)

    def get_rating(self, obj):
        return obj.rating

    class Meta(BaseSerializer.Meta):
        model = Department
        fields = ('id', 'name', 'desc', 'avatar',
                  'rating', 'users', 'achievements')


class AttachmentSerializer(BaseSerializer):
    path = fields.FileField(allow_empty_file=False, use_url=True)
    file_name = fields.SerializerMethodField(read_only=True)

    def get_file_name(self, obj):
        return os.path.basename(obj.path.name)

    class Meta(BaseSerializer.Meta):
        model = Attachment
        fields = ('id', 'path', 'file_name', 'mime_type')


class RequestSerializer(BaseSerializer):
    attachments = AttachmentSerializer(many=True)
    type = serializers.SerializerMethodField()
    task = TaskSerializer()

    def get_type(self, obj):
        return obj.task.type

    class Meta(BaseSerializer.Meta):
        model = Request
        fields = ('id', 'status', 'type', 'task', 'attachments')


class TaskRequestSerializer(serializers.Serializer):
    task_id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    attachments = serializers.PrimaryKeyRelatedField(
        queryset=Attachment.objects.all(), many=True
    )

    def create(self, validated_data):
        attach_ids = self._normalize_validated_data(validated_data)
        request_ = Request.objects.create(**validated_data)
        self._update_attachments(attach_ids, request_)
        request_.save()
        return request_

    def update(self, instance, validated_data):
        attach_ids = self._normalize_validated_data(validated_data)
        self._update_attachments(attach_ids, instance)
        instance.save(**validated_data)
        return instance

    @staticmethod
    def _update_attachments(attach_ids, request_):
        attach_models = Attachment.objects.filter(id__in=attach_ids)
        for model in attach_models:
            model.request = request_
            model.save()

    @staticmethod
    def _normalize_validated_data(validated_data):
        attach_ids = map(lambda a: a.id, validated_data.pop('attachments'))
        for key in ('task_id', 'user_id'):
            validated_data[key] = validated_data.pop(key).id
        return attach_ids


class BalanceLogSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = BalanceLog
