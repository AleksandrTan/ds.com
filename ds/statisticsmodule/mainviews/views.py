from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.shortcuts import render

from dsadminvn.mainviews.views import BaseAdminView
from dsstore.models import Products
from handsale.models import ProductsSale
from dsadminvn.forms import FilterSaleProduct


class DayStatistics(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'daystatistics.html'

    def get_context_data(self, **kwargs):
        context = super(DayStatistics, self).get_context_data(**kwargs)
        context['sale_list'] = ProductsSale.objects.day_statistics_sales()
        context['returns_list'] = ProductsSale.objects.day_statistics_returns()
        context['sum_sales_day'] = ProductsSale.objects.sum_sales_day()
        context['sum_returns_day'] = ProductsSale.objects.sum_returns_day()
        context['clear_sum'] = int(context['sum_sales_day']['price_per_page']) - int(context['sum_returns_day']['price_per_page'])
        context['tab_statistics'] = True
        return context


class PeriodStatistics(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'datestatistics.html'

    def get_context_data(self, **kwargs):
        context = super(PeriodStatistics, self).get_context_data(**kwargs)
        context['tab_statistics'] = True

        return context

    def get(self, request, *args, **kwargs):
        """
        If submit search form, add more options
        """
        if request.GET.getlist('submit'):
            form = FilterSaleProduct(request.GET)
            if form.is_valid():
                context = self.get_context_data()
                context['sum_sales_period'] = ProductsSale.objects.filterstat_date_sales(form.cleaned_data)
                context['sum_returns_period'] = ProductsSale.objects.filterstat_date_return(form.cleaned_data)
                if context['sum_sales_period']['price_per_page'] and context['sum_returns_period']['price_per_page']:
                    context['clear_sum'] = int(context['sum_sales_period']['price_per_page']) - int(context['sum_returns_period']['price_per_page'])
                context['data_form'] = form.cleaned_data
                return render(request, self.template_name, context)
            else:
                context = self.get_context_data()
                context['data_form'] = form.cleaned_data
                return render(request, self.template_name, context)
        else:
            context = self.get_context_data()
            context['sum_sales_period'] = ProductsSale.objects.filterstat_date_sales()
            context['sum_returns_period'] = ProductsSale.objects.filterstat_date_return()
            context['clear_sum'] = int(context['sum_sales_period']['price_per_page']) - int(context['sum_returns_period']['price_per_page'])
            return render(request, self.template_name, context)
