from rest_framework import generics
from api.models import User, Achievement, Request, Task
from api.serializers import AchievementSerializer


class UserAchievementsList(generics.ListAPIView):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        req = self.request

        try:
            user = User.objects.get(id=req.GET['id'])
        except KeyError:
            user = req.user
        except User.DoesNotExist:
            return Achievement.objects.none()

        tasks = Task.objects.filter(
            requests__user=user,
            requests__status=Request.REQUEST_STATUSES[1][0]
        )
        return Achievement.objects.filter(tasks__in=tasks)
