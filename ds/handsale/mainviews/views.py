from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import render
from dsadminvn.mainviews.views import BaseAdminView

from dsstore.models import Products
from handsale.models import ProductsSale, ProductsSellForm

class SellProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = "auth.change_user"
    form_class = ProductsSellForm
    template_name = 'producthandsell.html'
    succes_url = '/adminnv/products/'

    context_object_name = 'product_data'

    def get_context_data(self, **kwargs):
        context = super(SellProduct, self).get_context_data(**kwargs)
        context['tab_products'] = True

        return context

    def get(self, request, **kwargs):
        self.object = self.get_queryset(kwargs['pk'])
        return render(request, self.template_name, self.get_context_data())

    def get_queryset(self, pk):
        return Products.objects.get_single_product(pk)