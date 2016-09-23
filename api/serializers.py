from rest_framework import serializers
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 1
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


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    def get_progress(self, obj):
        pass

    def get_user_progress(self, obj):
        pass

    class Meta:
        model = Task
        depth = 1
        fields = ('id', 'name', 'desc', 'type', 'total_count', )


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        depth = 1
        fields = '__all__'
