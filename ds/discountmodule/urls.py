from django.conf.urls import url
from discountmodule.mainviews import views as discountviews

urlpatterns = [
    url(r'^discopage/$', discountviews.DiscountsPage.as_view(), name='discopage'),
    url(r'^discolist/$', discountviews.DiscountList.as_view(), name='discolist'),
    url(r'^filter/$', discountviews.SetDiscountFilter.as_view(), name='discountfilter'),
    url(r'^deletediscount/(?P<pk>\d+)/$', discountviews.DeleteDiscounts.as_view(), name='deletedisco'),
]