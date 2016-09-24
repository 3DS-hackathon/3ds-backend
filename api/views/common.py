from rest_framework import generics
from api.models import User


class RetrieveModelView(generics.RetrieveAPIView):
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        request = self.request

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = (request.GET.get(lookup_url_kwarg, None)
                        or self._guard_get_id())

        filter_kwargs = {self.lookup_field: lookup_value}

        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj

    def get_default_id(self):
        return None

    def _guard_get_id(self):
        try:
            return self.get_default_id()
        except:
            return -1


class UserFilterListView(generics.ListAPIView):
    def get_user(self):
        req = self.request
        try:
            user = User.objects.get(id=req.GET['id'])
        except KeyError:
            user = req.user
        except User.DoesNotExist:
            return None
        return user

