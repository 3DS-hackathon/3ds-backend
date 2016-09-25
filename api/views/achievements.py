from api.serializers import AchievementSerializer
from .common import UserFilterListView
from django.http import Http404


class UserAchievementsList(UserFilterListView):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        user = self.get_user()
        if user is None:
            raise Http404
        return user.achievements
