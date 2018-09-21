from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from dsadminvn.mainviews.views import BaseAdminView

from dsstore.models import Products
from handsale.models import ProductsSale


class DayStatistics(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'daystatistics.html'
    context_object_name = 'sale_list'
    queryset = ProductsSale.objects.day_statistics()

    def get_context_data(self, **kwargs):
        context = super(DayStatistics, self).get_context_data(**kwargs)
        context['tab_statistics'] = True
        return context


class PeriodStatistics(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):
    pass