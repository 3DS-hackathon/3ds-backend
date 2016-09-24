from rest_framework import generics
from api.models import BalanceLog, User
from api.serializers import BalanceLogSerializer


class UserBalanceLogList(generics.ListAPIView):
    queryset = BalanceLog.objects.all()
    serializer_class = BalanceLogSerializer

    def filter_queryset(self, queryset):
        req = self.request

        try:
            user = User.objects.get(id=req.GET['id'])
        except KeyError:
            user = req.user
        except User.DoesNotExist:
            return queryset.none()

        return queryset.filter(request__task__in=(user.tasks.all()))
