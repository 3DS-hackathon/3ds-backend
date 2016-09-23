from django.conf.urls import url
from .views.users import UserList, TaskList


urlpatterns = [
    url(r'^login$', UserList.as_view(), id=1),
]
