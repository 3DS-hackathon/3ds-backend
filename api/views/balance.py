from rest_framework import generics
from api.models import BalanceLog, User
from api.serializers import BalanceLogSerializer


class UserBalanceLogList(generics.ListAPIView):
    queryset = BalanceLog.objects.all()
    serializer_class = BalanceLogSerializer

    def filter_queryset(self, queryset):
        req = self.request
        user = User.objects.filter(id=req.GET.get('id')).first() or req.user

        if not user:
            return queryset.none()
        return queryset.filter(task__in=(user.tasks.filter()))
