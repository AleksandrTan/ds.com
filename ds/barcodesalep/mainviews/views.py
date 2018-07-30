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
            product_result = Products.objects.check_isset_pre_barcode(kwargs['pre_barcode'])
        return JsonResponse({"status": product_result})