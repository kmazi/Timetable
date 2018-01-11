from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.HomePage.as_view()),
    url(r'^timetable/$', views.ShowTable.as_view()),
    url(r'^timetable/(?P<department_id>\d)/(?P<level>\d)/$', views.LevelTimetable.as_view()),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout, {'next_page':'/'}, name='logout'),
]