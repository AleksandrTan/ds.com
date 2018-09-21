from django.conf.urls import url
from statisticsmodule.mainviews import views as viewsstatistics

urlpatterns = [
    url(r'^daystatistics/$', viewsstatistics.DayStatistics.as_view(), name='daystatistics'),
    url(r'^periodstatistics/(?:page/(?P<page>\d+)/)?$', viewsstatistics.PeriodStatistics.as_view(), name='periodstatistics'),
]