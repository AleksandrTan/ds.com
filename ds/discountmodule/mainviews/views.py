from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect

from dsadminvn.mainviews.views import BaseAdminView
from dsstore.models import (MainCategory, NameProduct, Brends, Seasons, Products)
from discountmodule.models import Discounts
from discountmodule.forms import FilterDiscounts


class DiscountsPage(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'discountadd.html'

    def get_context_data(self, **kwargs):
        context = super(DiscountsPage, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_discounts'] = True

        return context


class SetDiscountFilter(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'discountshow.html'

    def get_context_data(self, **kwargs):
        context = super(SetDiscountFilter, self).get_context_data(**kwargs)
        context['tab_discounts'] = True

        return context

    def post(self, request, *args, **kwargs):
        form = FilterDiscounts(request.POST)
        if form.is_valid():
            disco_val = form.cleaned_data['disco_value']
            description = form.cleaned_data['description_f']
            form.cleaned_data.pop('disco_value')
            form.cleaned_data.pop('description_f')
            list_id = Products.objects.set_discount_products(form.cleaned_data, disco_val)
            if list_id:
                Discounts.objects.save_discount(list_id, description, disco_val)
                return redirect('/adminnv/products/discount/discopage/')
            else:
                return redirect('/adminnv/products/')
        else:
            self.data = form.cleaned_data
            context = dict()
            context['maincategorys'] = MainCategory.objects.get_active_categories()
            context['nameproducts'] = NameProduct.objects.get_active_products()
            context['brends'] = Brends.objects.get_active_brends()
            context['seasons'] = Seasons.objects.get_active_seasons()
            context['form_data'] = self.data
            context['form_errors'] = form.errors['disco_value']
            return render(request, 'discountadd.html', context)


class SetDiscountArticul(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    pass


class SetDiscountModel(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    pass


class DeleteDiscounts(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):
    pass


class DiscountList(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    pass