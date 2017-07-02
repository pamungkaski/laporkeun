from django.conf.urls import url

from task import apps
from . import views

app_name = apps.TaskConfig.name
urlpatterns = [
    url(r'^crt/(?P<pk_project>[\w]+)/$', views.TaskCreationView.as_view(),
        name='creation'),
    url(r'^la/$', views.TaskAssignedListView.as_view(),
        name='assigned'),
    url(r'^lp/(?P<pk_project>[\w]+)/$', views.TaskProjectListView.as_view(),
        name='project'),
    url(r'^(?P<pk>[\w]+)/asg/$', views.TaskAssignedView.as_view(),
        name='assign'),
    url(r'^(?P<pk>[\w]+)/del/$', views.TaskDeleteView.as_view(),
        name='delete'),
    url(r'^(?P<pk>[\w]+)/edi/$', views.TaskEditView.as_view(),
        name='edit'),
    url(r'^(?P<pk>[\w]+)/$',views.TaskDetailView.as_view(),
        name='detail'),
]
