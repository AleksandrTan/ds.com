import io
from django.http import StreamingHttpResponse
import xlsxwriter
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.template import loader, Context

from dsadminvn.mainviews.views import BaseAdminView
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
        if context['sum_sales_day']['price_per_page'] and context['sum_returns_day']['price_per_page']:
            context['clear_sum'] =int(context['sum_sales_day']['price_per_page']) - int(context['sum_returns_day']['price_per_page'])
        else:
            context['clear_sum'] = '0'
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
                else:
                    context['clear_sum'] = '0'
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
            if context['sum_sales_period']['price_per_page'] and context['sum_returns_period']['price_per_page']:
                context['clear_sum'] = int(context['sum_sales_period']['price_per_page']) - int(context['sum_returns_period']['price_per_page'])
            else:
                context['clear_sum'] = 0
            return render(request, self.template_name, context)


class GetSCVFile(BaseAdminView):
    def get(self, request):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        header_format = workbook.add_format({'bold': True,
                                     'align': 'center',
                                     'valign': 'vcenter',
                                     'fg_color': '#D7E4BC',
                                     'border': 1})
        data = [
            [1, 10000, 5000, 8000, 6000, 9, 9, 8, 8, 0],
            [2, 2000, 3000, 4000, 5000, 9, 9, 8, 8, 0],
            [3, 6000, 6000, 6500, 6000, 9, 9, 8, 8, 0],
            [4, 500, 300, 200, 700, 9, 9, 8, 8, 0],
        ]
        caption = 'Статистика продаж за день.'
        worksheet.set_row(0, 30)
        worksheet.set_column('D:H', 12)
        worksheet.merge_range('D1:H1', caption, header_format)
        # Write the caption.
        #worksheet.write('B1', caption, header_format)
        # Set the columns widths.
        worksheet.set_column('B:K', 12)
        # Add a table to the worksheet.
        worksheet.add_table('B3:K7', {'data': data,
                                      'total_row': 1,
                                      'columns': [{'header': 'Товар'},
                                                  {'header': 'Артикул'},
                                                  {'header': 'Колличество'},
                                                  {'header': 'Цена'},
                                                  {'header': 'Скидка'},
                                                  {'header': 'Уступили'},
                                                  {'header': 'Итоговая цена'},
                                                  {'header': 'Место продажи'},
                                                  {'header': 'Дата продажи'},
                                                  {'header': 'Описание'}
                                                  ]
                                      })
        workbook.close()
        output.seek(0)

        # Set up the Http response.
        filename = 'daystatistics.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response