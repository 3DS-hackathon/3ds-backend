from api.models import BalanceLog
from api.serializers import BalanceLogSerializer
from .common import UserFilterListView


class UserBalanceLogList(UserFilterListView):
    queryset = BalanceLog.objects.all()
    serializer_class = BalanceLogSerializer

    def filter_queryset(self, queryset):
        user = self.get_user()
        if user is None:
            return queryset.none()
        return queryset.filter(request__task__in=(user.tasks.all()))

