from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.shortcuts import render

from dsadminvn.mainviews.views import BaseAdminView
from dsstore.models import (MainCategory, NameProduct, Brends, Seasons)
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


class SetDiscountFilter(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'discountshow.html'

    def get_context_data(self, **kwargs):
        context = super(SetDiscountFilter, self).get_context_data(**kwargs)
        context['tab_discounts'] = True

        return context

    def get(self, request, *args, **kwargs):
        """
        If submit search form, add more options
        """
        form = FilterDiscounts(request.GET)
        if form.is_valid():
            self.data = form.cleaned_data
            self.object_list = self.get_queryset()
            context = self.get_context_data(object_list=self.object_list)
            context['data_form'] = form.cleaned_data
            copy_get = QueryDict(request.GET.copy().urlencode(), mutable=True)
            copy_get['submit'] = 0
            context['request_get'] = copy_get.urlencode()
            return render(request, self.template_name, context)
        else:
            self.data = form.cleaned_data
            self.object_list = self.get_queryset()
            context = self.get_context_data(object_list=self.object_list)
            context['form'] = form
            return render(request, self.template_name, context)

class SetDiscountArticul(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    pass


class SetDiscountModel(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    pass


class DeleteDiscounts(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):
    pass


class DiscountList(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    pass