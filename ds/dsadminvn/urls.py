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
    url(r'^ajax/getsizes/(?P<pk>[0-9]+)/$', views.AjaxGetSizes.as_view(), name='ajax_st_get'),
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

"""
    URL`s for Seasons
"""
se_patterns = [
    url(r'^ajax/isactive/(?P<pk>[0-9]+)/$', views.AjaxSeasonActive.as_view(), name='ajax_se_is_active'),
    url(r'^ajax/addnew/$', views.AjaxSeasonNew.as_view(), name='ajax_se_new'),
    url(r'^deletese/(?P<pk>[0-9]+)/$', views.SeasonDelete.as_view(), name='delete_se'),
    url(r'^$', views.SeasonsWork.as_view(), name='seasons'),
]

"""
    URL`s for Products
"""
pr_patterns = [
    url(r'^(?:page/(?P<page>\d+)/)?$', views.ProductsWork.as_view(), name='products'),
    url(r'^addproduct/$', views.CreateNewProduct.as_view(), name='showform_for_add_product'),
    url(r'^createproduct/$', views.CreateNewProduct.as_view(), name='createproduct'),
    url(r'^viewproduct/(?P<pk>\d+)/$', views.ViewProduct.as_view(), name="viewproduct"),
    url(r'^edit/(?P<pk>\d+)/$', views.EditProduct.as_view(), name='editproduct'),
    url(r'^checkarticul/(?P<articul>\w+)/$', views.CheckIssetArticul.as_view()),
    url(r'^deleteproduct/(?P<pk>\d+)/$', views.DeleteProduct.as_view(), name='deleteproduct'),
    url(r'^foundproduct/$', views.FoundArticul.as_view(), name='foundproduct'),
    url(r'^filterproduct/(?:page/(?P<page>\d+)/)?$', views.FilterProduct.as_view(), name='filterproduct')
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
    url(r'^adminnv/products/', include(pr_patterns)),
    url(r'^adminnv/seasons/', include(se_patterns)),
]

