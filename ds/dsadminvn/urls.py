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
    URL`s for Msn (MainCategory, Size, NameProduct)
"""
mc_patterns = [
    # url(r'^ajaxctr/isactive/(?P<pk>[0-9]+)/$', views.AjaxCtrActive.as_view(), name='ajax_ctr_is_active'),
     url(r'^ajax/addnew/$', views.AjaxMainCategoryNew.as_view(), name='ajax_mc_new'),
    # url(r'^deletectr/(?P<pk>[0-9]+)/$', views.CtrDelete.as_view(), name='delete_ctr'),
    # url(r'^ajaxctr/newnum/$', views.AjaxNumNewCategories.as_view(), name='ajax_new_num'),
    # url(r'^ajax/newsentcount/$', views.AjaxNewSentencesView.as_view(), name='get_new_count'),
    # url(r'^modesentence/$', views.ModerateNewSentence.as_view(), name='mode_new_sentence'),
    # url(r'^moderesult/(?P<status>[0-9]{1})/(?P<pk>[0-9]+)/$', views.ModeResult.as_view(), name='moderesult'),
    url(r'^$', views.MainCategoryWork.as_view(), name='maincategory'),
]

urlpatterns = [
    url(r'^loginadmin/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/loginadmin'}, name='logout'),
    url(r'^adminnv/$', views.MainView.as_view(), name='homeadmin'),
    url(r'^adminnv/users/', include(users_patterns)),
    url(r'^adminnv/maincategory/', include(mc_patterns)),
]

