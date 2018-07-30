from django.conf.urls import url
from handsale.mainviews import views as viewshandsale

urlpatterns = [
    url(r'^sellproduct/(?P<pk>\d+)/$', viewshandsale.SellProduct.as_view(), name='sellproduct'),
    url(r'^returnsell/(?P<pk>\d+)/(?P<plase_pk>\d+)/$', viewshandsale.ReturnSale.as_view(), name='returnsale'),
]