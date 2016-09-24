from rest_framework import generics, views, status
from rest_framework.response import Response
from api.models import User, Task, TaskStatus
from api.serializers import UserSerializer, TaskSerializer
from .common import RetrieveModelView


class UserView(RetrieveModelView):
    lookup_url_kwarg = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_default_id(self):
        return self.request.user.id


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskAcceptor(views.APIView):

    def get(self, request, format=None):
        task = Task.objects.get(id=request.GET.get('id'))
        user = request.user
        TaskStatus.create(user, task)
        serializer = TaskSerializer(instance=task)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTaskList(TaskList):

    def filter_queryset(self, queryset):
        user = self.request.user
        if not user:
            return queryset.none()
        return queryset.filter(task_status__user=user)
