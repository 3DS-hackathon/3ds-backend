from rest_framework import generics
from api.models import User, Task
from api.serializers import UserSerializer, TaskSerializer


class UserList(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskList(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

