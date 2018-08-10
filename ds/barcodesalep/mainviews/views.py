from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from dsadminvn.mainviews.views import BaseAdminView

from dsstore.models import Products, SizeCount


class BarcodeSalePage(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'barcodesalep.html'


class GetSaleProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            product_result = Products.objects.get_product_barcode(kwargs['identifier'])
            if product_result['status']:
                return JsonResponse({"status": True, 'data_product': product_result['data_product'].id})
            else:
                return JsonResponse({"status": False})