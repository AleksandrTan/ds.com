from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
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
    succes_url = '/adminnv/products/viewproduct/'
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
        context['price_discount'] = self.object.price if self.object.discount == 0 else \
            self.object.price - ((self.object.price * self.object.discount) / 100)
        context['action'] = reverse('sellproduct',
                                    kwargs={'pk': kwargs['pk']})

        return render(request, self.template_name, context)

    def get_queryset(self, pk):
        return Products.objects.get_single_product(pk)

    def form_valid(self, form):
        self.object = form.cleaned_data['products']
        import copy
        for i in range(int(form.cleaned_data['count_num'])):
            forma = copy.deepcopy(form)
            self.saved_data(forma)

        #return super(SellProduct, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def saved_data(self, forma):
        instance = forma.save(commit=False)
        instance.count_num = 1
        instance.link_name = ''
        #product = Products.objects.get_single_product(self.kwargs['pk'])
        instance.articul = instance.products.articul
        instance.size = instance.products.size
        instance.purshase_price = instance.products.purshase_price
        instance.products = instance.products
        if forma.cleaned_data['lost_num'] and instance.products.discount:
            instance.lost_num = forma.cleaned_data['lost_num']
            instance.true_price = (instance.products.price - ((instance.products.price * instance.products.discount) / 100)) - forma.cleaned_data['lost_num']
        elif forma.cleaned_data['lost_num'] and not instance.products.discount:
            instance.lost_num = forma.cleaned_data['lost_num']
            instance.true_price = forma.cleaned_data['price'] - forma.cleaned_data['lost_num']
        elif not forma.cleaned_data['lost_num'] and instance.products.discount:
            instance.true_price = instance.products.price - ((instance.products.price * instance.products.discount) / 100)
        else:
            instance.true_price = forma.cleaned_data['price']
        instance.total_amount = instance.true_price
        instance.discount = instance.products.discount
        instance.save()
        # reduce the amount of product
        Products.objects.reduce_amount(instance.products.id, 1)

    def form_invalid(self, form):
        self.object = form.cleaned_data['products']
        context = self.get_context_data()
        context['tab_products'] = True

        return self.render_to_response(context)

    def get_success_url(self):
        return self.succes_url+'{0}'.format(self.object.id)


class ReturnSale(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    login_url = 'login'
    permission_required = "auth.change_user"
    url = '/adminnv/products/saleviewproduct/%s/'

    def get_redirect_url(self, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the
        URL pattern match generating the redirect request
        are provided as kwargs to this method.
        """
        if self.url:
            url = self.url % kwargs['pk']
            return url
        else:
            return None

    def get(self, request, *args, **kwargs):
        ProductsSale.objects.return_sale(kwargs['plase_pk'], kwargs['pk'])
        return super(ReturnSale, self).get(request, *args, **kwargs)
