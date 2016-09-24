from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = format_suffix_patterns([
    url(r'^user/tasks$', UserTaskList.as_view()),
    url(r'^user/log$', UserBalanceLogList.as_view()),
    url(r'^user/achievements$', UserAchievementsList.as_view()),

    url(r'^task$', TaskAcceptor.as_view()),
    url(r'^login$', ObtainTokenView.as_view()),
    url(r'^attach$', AttachmentCreator.as_view()),
    url(r'^request$', RequestCreator.as_view()),

    url(r'^user$', UserView.as_view()),
    url(r'^tasks$', TaskList.as_view()),
    url(r'^department$', DepartmentView.as_view()),
])

