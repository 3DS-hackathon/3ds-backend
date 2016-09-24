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

    class Meta(BaseSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
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
                  'experience', 'price', 'requests')


class TaskStatusSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TaskStatus
        exclude = ('user',)


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

    def create(self, validated_data):
        request_ = Request.objects.create(**validated_data)
        attach_ids = validated_data.pop('attachments', [])
        self._update_attachments(attach_ids, request_)
        request_.save()
        return request_

    def update(self, instance, validated_data):
        attach_ids = validated_data.pop('attachments', [])
        self._update_attachments(attach_ids, instance)
        instance.save(**validated_data)
        return instance

    @staticmethod
    def _update_attachments(attach_ids, request_):
        attach_models = Attachment.objects.filter(id__in=attach_ids)
        for model in attach_models:
            model.request = request_
            model.save()

    class Meta(BaseSerializer.Meta):
        model = Request
        fields = ('id', 'data_balance', 'status',
                  'type', 'task', 'attachments')


class AchievementSerializer(BaseSerializer):
    pic = fields.FileField(allow_empty_file=False, use_url=True)

    class Meta(BaseSerializer.Meta):
        model = Achievement
        fields = ('id', 'name', 'desc', 'pic', 'users', 'tasks')


class BalanceLogSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = BalanceLog
