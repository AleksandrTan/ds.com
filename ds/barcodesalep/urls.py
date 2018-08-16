from django.conf.urls import url
from barcodesalep.mainviews import views

urlpatterns = [
    url(r'^page/$', views.BarcodeSalePage.as_view(), name='barcodepage'),
    url(r'^getproduct/(?P<identifier>.*)/$', views.GetSaleProduct.as_view(), name='barcodegetproduct'),
]