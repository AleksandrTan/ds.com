from django.conf.urls import url
from modelssmodule.mainviews import views


urlpatterns = [
    url(r'^(?:page/(?P<page>\d+)/)?$', views.ModelssWork.as_view(), name='modelss'),
    url(r'^addmodelss/$', views.CreateNewModelss.as_view(), name='showform_for_add_modelss'),
    url(r'^createmodelss/$', views.CreateNewModelss.as_view(), name='createmodelss'),
    url(r'^foundmodelss/$', views.FoundsModelss.as_view(), name='foundmodelss'),
    url(r'^edit/(?P<pk>\d+)/$', views.EditModelss.as_view(), name='editmodelss'),
    url(r'^deletemodelss/(?P<pk>\d+)/$', views.DeleteModelss.as_view(), name='deletemodelss'),
    url(r'^viewmodelss/(?P<pk>\d+)/$', views.ViewModelss.as_view(), name="viewmodelss"),
    # url(r'^foundproduct/$', views.FoundArticul.as_view(), name='foundproduct'),
    # url(r'^foundmodelss/$', views.FoundsModelss.as_view(), name='foundmodelss'),
    # url(r'^filterproduct/(?:page/(?P<page>\d+)/)?$', views.FilterProduct.as_view(), name='filterproduct'),
    # url(r'^saleviewproduct/(?P<pk>\d+)/(?:page/(?P<page>\d+)/)?$', views.SaleViewProduct.as_view(), name='saleproductview'),
]