from django.conf.urls import url
from django.contrib.auth import views as auth_views

from project import apps, views

app_name = apps.ProjectConfig.name
urlpatterns = [
    url(r'^crt/$', views.ProjectCreationView.as_view(),
        name='creation'),
    url(r'^la/$', views.ProjectAdminListView.as_view(),
        name='administered'),
    url(r'^lm/$', views.ProjectMemberListView.as_view(),
        name='member'),
    url(r'^(?P<pk>[\w]+)/lm/$', views.ProjectMemberListView.as_view(),
        name='list_member'),
    url(r'^(?P<pk>[\w]+)/adm/$', views.ProjectAdminView.as_view(),
        name='edit_admin'),
    url(r'^(?P<pk>[\w]+)/mbr/$', views.ProjectMemberView.as_view(),
        name='edit_member'),
    url(r'^(?P<pk>[\w]+)/del/$', views.ProjectDeleteView.as_view(),
        name='delete'),
    url(r'^(?P<pk>[\w]+)/edi/$', views.ProjectEditView.as_view(),
        name='edit'),
    url(r'^(?P<pk>[\w]+)/$', views.ProjectDetailView.as_view(),
        name='detail'),
]
