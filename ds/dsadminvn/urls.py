from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from dsadminvn.mainviews import views

"""
    URL`s for Users site
"""
users_patterns = [
    url(r'^(?:page/(?P<page>\d+)/)?$', views.UsersWork.as_view(), name='users'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='detail'),
]

"""
    URL`s for Main Category
"""
mc_patterns = [
     url(r'^ajax/isactive/(?P<pk>[0-9]+)/$', views.AjaxMainCategoryActive.as_view(), name='ajax_mc_is_active'),
     url(r'^ajax/addnew/$', views.AjaxMainCategoryNew.as_view(), name='ajax_mc_new'),
     url(r'^deletemc/(?P<pk>[0-9]+)/$', views.MainCategoryDelete.as_view(), name='delete_mc'),
     url(r'^$', views.MainCategoryWork.as_view(), name='maincategory'),
]

"""
    URL`s for Name Product
"""
np_patterns = [
     url(r'^ajax/isactivenp/(?P<pk>[0-9]+)/$', views.AjaxNameProductActive.as_view(), name='ajax_np_is_active'),
     url(r'^ajax/addnewproduct/$', views.AjaxNameProductNew.as_view(), name='ajax_np_new'),
     url(r'^deletenp/(?P<pk>[0-9]+)/$', views.NameProductDelete.as_view(), name='delete_np'),
     url(r'^(?:page/(?P<page>\d+)/)?$', views.NameProductWork.as_view(), name='nameproduct'),
]

"""
    URL`s for Size Table
"""
st_patterns = [
     url(r'^addnew/$', views.SizeTableAddNew.as_view(), name='st_add_new'),
     url(r'^delete/(?P<pk>[0-9]+)/$', views.SizeTableDelete.as_view(), name='delete_st'),
     url(r'^$', views.SizeTableWork.as_view(), name='sizetable'),
]

"""
    URL`s for Brends
"""
br_patterns = [
     url(r'^ajax/isactive/(?P<pk>[0-9]+)/$', views.AjaxBrendActive.as_view(), name='ajax_br_is_active'),
     url(r'^ajax/addnew/$', views.AjaxBrendNew.as_view(), name='ajax_br_new'),
     url(r'^deletebr/(?P<pk>[0-9]+)/$', views.BrendDelete.as_view(), name='delete_br'),
     url(r'^$', views.BrendsWork.as_view(), name='brends'),
]

urlpatterns = [
    url(r'^loginadmin/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/loginadmin'}, name='logout'),
    url(r'^adminnv/$', views.MainView.as_view(), name='homeadmin'),
    url(r'^adminnv/users/', include(users_patterns)),
    url(r'^adminnv/maincategory/', include(mc_patterns)),
    url(r'^adminnv/nameproduct/', include(np_patterns)),
    url(r'^adminnv/sizetable/', include(st_patterns)),
    url(r'^adminnv/brends/', include(br_patterns)),
]

