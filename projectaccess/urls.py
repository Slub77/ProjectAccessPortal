from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users, name='users'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^import/$', views.import_users_and_projects, name='import'),
    url(r'^update_p4/$', views.update_p4, name='update_p4'),
]
