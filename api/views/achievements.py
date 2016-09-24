from api.models import Achievement, Request, Task
from api.serializers import AchievementSerializer
from .common import UserFilterListView


class UserAchievementsList(UserFilterListView):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        user = self.get_user()
        tasks = Task.objects.filter(
            requests__user=user,
            requests__status=Request.REQUEST_STATUSES[1][0]
        )
        return Achievement.objects.filter(tasks__in=tasks)
