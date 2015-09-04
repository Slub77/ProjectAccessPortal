from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users, name='users'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^import_p4_users/$', views.import_p4_users, name='import_p4_users'),
    url(r'^create_new_project/$', views.create_new_project, name='create_new_project'),
    url(r'^create_new_project_submit/$', views.create_new_project_submit, name='create_new_project_submit'),
    url(r'^(?P<id>[0-9]+)/delete_project/$', views.delete_project, name='delete_project'),
]
