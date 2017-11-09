from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from dsadminvn.mainviews import views

"""
    URL`s for Users site
"""
users_patterns = [
    url(r'^(?:page/(?P<page>\d+)/)?$', views.UsersWork.as_view(), name='users'),
]



urlpatterns = [
    url(r'^loginadmin/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^$', views.MainView.as_view(), name='home'),
    url(r'^users/', include(users_patterns)),
]

