from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.core.urlresolvers import reverse
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
        context['action'] = reverse('sellproduct',
                                    kwargs={'pk': kwargs['pk']})

        return context
    """
        Show form for sell product with data produc
    """
    def get(self, request, **kwargs):
        self.object = self.get_queryset(kwargs['pk'])
        return render(request, self.template_name, self.get_context_data())

    def get_queryset(self, pk):
        return Products.objects.get_single_product(pk)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.link_name = ''
        product = Products.objects.get_single_product(form.cleaned_data['products'])
        instance.products = product
        instance.save()

        return super(SellProduct, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['tab_products'] = True

        return self.render_to_response(context)