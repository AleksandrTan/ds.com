from django.conf.urls import url
from modelssmodule.mainviews import views


urlpatterns = [
    url(r'^(?:page/(?P<page>\d+)/)?$', views.ModelssWork.as_view(), name='modelss'),
    url(r'^addmodelss/$', views.CreateNewModelss.as_view(), name='showform_for_add_modelss'),
    url(r'^createmodelss/$', views.CreateNewModelss.as_view(), name='createmodelss'),
    # url(r'^viewproduct/(?P<pk>\d+)/$', views.ViewProduct.as_view(), name="viewproduct"),
    # url(r'^edit/(?P<pk>\d+)/$', views.EditProduct.as_view(), name='editproduct'),
    # url(r'^checkarticul/(?P<articul>\w+)/$', views.CheckIssetArticul.as_view()),
    # url(r'^checkprebarcode/(?P<pre_barcode>\w+)/$', views.CheckIssetPreBarcode.as_view()),
    # url(r'^checkmodelss/(?P<modelss>\w+)/$', views.CheckIssetModelss.as_view()),
    # url(r'^deleteproduct/(?P<pk>\d+)/$', views.DeleteProduct.as_view(), name='deleteproduct'),
    # url(r'^foundproduct/$', views.FoundArticul.as_view(), name='foundproduct'),
    # url(r'^foundmodelss/$', views.FoundsModelss.as_view(), name='foundmodelss'),
    # url(r'^filterproduct/(?:page/(?P<page>\d+)/)?$', views.FilterProduct.as_view(), name='filterproduct'),
    # url(r'^saleviewproduct/(?P<pk>\d+)/(?:page/(?P<page>\d+)/)?$', views.SaleViewProduct.as_view(), name='saleproductview'),
]