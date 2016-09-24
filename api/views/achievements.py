from rest_framework import generics
from api.models import User
from api.serializers import AchievementSerializer


class UserAchievementsList(generics.ListAPIView):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        req = self.request
        user = User.objects.filter(id=req.GET.get('id')).first() or req.user
        return user.achievements.all()
