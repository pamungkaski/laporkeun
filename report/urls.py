from django.conf.urls import url

from . import apps
from . import views

app_name = apps.ReportConfig.name
urlpatterns = [
    url(r'^crt/(?P<pk_task>[\w]+)/$', views.ReportCreationView.as_view(),
        name='creation'),
    url(r'^lm/$', views.ReportMemberListView.as_view(),
        name='reporter'),
    url(r'^lt/(?P<pk_task>[\w]+)/$', views.ReportTaskListView.as_view(),
        name='task'),
    url(r'^(?P<pk>[\w]+)/upd/$', views.ReportUpdateView.as_view(),
        name='update'),
]
