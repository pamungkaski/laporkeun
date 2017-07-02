from django.conf.urls import url
from django.contrib.auth import views as auth_views

from member import apps, views

app_name = apps.MemberConfig.name
urlpatterns = [
    url(r'^i/$', auth_views.login, {
        'template_name': 'member/login.html',
        'redirect_authenticated_user': True,
    }, name='login'),
    url(r'^o/$', auth_views.logout,
        name='logout'),
    url(r'^pc/$', auth_views.password_change, {
        'template_name': 'member/password_change.html',
        'post_change_redirect': 'home',
    }, name='password_change'),
    url(r'^pcd/$', auth_views.password_change_done, {
        'template_name': 'member/password_change_done.html',
        'current_app': 'member'
    }, name='password_change_done'),
    url(r'^crt/$', views.member_creation_view,
        name='creation'),
    url(r'^upd/$', views.MemberUpdateView.as_view(),
        name='update'),
]
