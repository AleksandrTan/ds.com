from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.core.urlresolvers import reverse
from dsadminvn.mainviews.views import BaseAdminView

from dsstore.models import Products, SizeCount
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
    """
        Show form for sell product with data product
    """
    def get(self, request, **kwargs):
        self.object = self.get_queryset(kwargs['pk'])
        context = self.get_context_data()
        context['action'] = reverse('sellproduct',
                                    kwargs={'pk': kwargs['pk']})

        return render(request, self.template_name, context)

    def get_queryset(self, pk):
        return Products.objects.get_single_product(pk)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.link_name = ''
        # product = Products.objects.get_single_product(form.cleaned_data['products'])
        instance.size = SizeCount.objects.get_single_size(form.cleaned_data['size'])
        instance.products = form.cleaned_data['products']
        instance.save()
        # reduce the amount of product
        SizeCount.objects.get_single_size(form.cleaned_data['size'], form.cleaned_data['count_num'])

        return super(SellProduct, self).form_valid(form)

    def form_invalid(self, form):
        self.object = form.cleaned_data['products']
        context = self.get_context_data()
        context['tab_products'] = True

        return self.render_to_response(context)

    def get_success_url(self):
        return self.succes_url