from django.conf.urls import url
from handsale.mainviews import views as viewshandsale

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', viewshandsale.SellProduct.as_view(), name='sellproduct'),
    url(r'^(?P<pk>\d+)/(?P<plase_pk>\d+)/$', viewshandsale.ReturnSale.as_view(), name='returnsale'),
]