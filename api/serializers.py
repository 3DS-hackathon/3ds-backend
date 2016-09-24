import os.path
from abc import ABCMeta
from rest_framework import serializers
from rest_framework import fields
from api.models import *


class BaseSerializer(serializers.ModelSerializer):
    class Meta(metaclass=ABCMeta):
        depth = 1
        fields = '__all__'


class LevelSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Level


class UserSerializer(BaseSerializer):
    level = LevelSerializer(source='get_level')
    avatar = fields.FileField(read_only=True, use_url=True)
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        return obj.get_balance()

    class Meta(BaseSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'full_name',
            'role',
            'department',
            'balance',
            'rating',
            'phone',
            'avatar',
            'tasks',
            'level',
            'achievements',
        )


class DepartmentSerializer(serializers.ModelSerializer):
    avatar = fields.FileField(read_only=True, use_url=True)

    class Meta:
        model = Department
        fields = ('id', 'name', 'desc', 'avatar', 'rating', 'users')


class TaskSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Task
        fields = ('id', 'name', 'desc', 'type', 'total_count',
                  'experience', 'price')


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
        attach_ids = map(lambda a: a.id, validated_data.pop('attachments'))
        validated_data['task_id'] = validated_data.pop('task_id').id
        validated_data['user_id'] = validated_data.pop('user_id').id
        request_ = Request.objects.create(**validated_data)
        self._update_attachments(attach_ids, request_)
        request_.save()
        return request_

    def update(self, instance, validated_data):
        attach_ids = map(lambda a: a.id, validated_data.pop('attachments'))
        validated_data['task_id'] = validated_data.pop('task_id').id
        validated_data['user_id'] = validated_data.pop('user_id').id
        self._update_attachments(attach_ids, instance)
        instance.save(**validated_data)
        return instance

    @staticmethod
    def _update_attachments(attach_ids, request_):
        attach_models = Attachment.objects.filter(id__in=attach_ids)
        for model in attach_models:
            model.request = request_
            model.save()


class AchievementSerializer(BaseSerializer):
    pic = fields.FileField(allow_empty_file=False, use_url=True)

    class Meta(BaseSerializer.Meta):
        model = Achievement
        fields = ('id', 'name', 'desc', 'pic', 'users', 'tasks')


class BalanceLogSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = BalanceLog
