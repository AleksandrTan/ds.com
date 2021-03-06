from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.generic.edit import CreateView

from dsadminvn.mainviews.views import BaseAdminView
from dsstore.models import Products
from handsale.models import ProductsBarcodeFormSet, ProductsSale


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
                return JsonResponse({"status": True, 'data_product': product_result['data_product']})
            else:
                return JsonResponse({"status": False})


class SaveProducts(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = "auth.change_user"
    succes_url = '/adminnv/products/barcode/page/'
    context_object_name = 'product_data'
    model = ProductsSale
    fields = ('products', 'lost_num', 'description')

    def form_valid(self, form):
        formset = ProductsBarcodeFormSet(self.request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.count_num = 1
                instance.link_name = ''
                instance.articul = instance.products.articul
                instance.size = instance.products.size
                instance.price = instance.products.price
                instance.purshase_price = instance.products.purshase_price
                instance.products = instance.products
                if instance.lost_num and instance.products.discount:
                    instance.lost_num = instance.lost_num
                    instance.true_price = (instance.products.price - ((instance.products.price * instance.products.discount) / 100)) - \
                                          instance.lost_num
                elif instance.lost_num and not instance.products.discount:
                    instance.lost_num = instance.lost_num
                    instance.true_price = instance.price - instance.lost_num
                elif not instance.lost_num and instance.products.discount:
                    instance.true_price = instance.products.price - ((instance.products.price * instance.products.discount) / 100)
                else:
                    instance.true_price = instance.price
                instance.total_amount = instance.true_price
                instance.discount = instance.products.discount
                instance.save()
                # reduce the amount of product
                Products.objects.reduce_amount(instance.products.id, 1)
        return super(SaveProducts, self).form_valid(formset)

    def get_success_url(self):
        return self.succes_url