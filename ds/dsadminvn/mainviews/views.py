import os
from datetime import timedelta, date

from django.conf import settings
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy, reverse

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import QueryDict

from django.contrib.auth.models import User, Group
from dsstore.models import (MainCategory, NameProduct, SizeTable,
                            SizeTableForm, Brends, Seasons, Products,
                            ProductsForm, ProductsFormEdit, Image, Modelss)
from handsale.models import ProductsSale
from dsadminvn.forms import FoundArticuls, FilterProducts, FilterSaleProduct
from modelssmodule.forms import FoundModelss
from dsadminvn.mainhelpers.SetBarcode import SetBarcode as SBS


class BaseAdminView(View):
    """
    Base view for admin views.
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    Look in Python3\Lib\site-packages\django\contrib\admin\views\decorators.py
            Python3\Lib\site-packages\django\contrib\auth\decorators.py
            Python3\Lib\site-packages\django\contrib\admindocs\views.py
            https://djbook.ru/rel1.9/ref/contrib/admin/index.html#the-staff-member-required-decorator
    """
    @method_decorator(staff_member_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(BaseAdminView, self).dispatch(request, *args, **kwargs)

#Class MainView  - start page


class MainView(BaseAdminView, LoginRequiredMixin, TemplateView):
   template_name = 'index.html'
   login_url = 'login'

   # def get(self, request, *args, **kwargs):
   #     send_mail('Subject here', 'Here is the message.', 'rumych2013@gmail.com',
   #               ['rumych2013@gmail.com'], fail_silently=False)
   #     return super(MainView, self).get(self, request, *args, **kwargs)

"""
    Work with users site
"""


class UsersWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

   permission_required = "auth.change_user"
   template_name = 'users/users.html'
   login_url = 'login'
   queryset = User.objects.all()
   context_object_name = 'users_list' #or for custom paginate page_obj in template
   paginate_by = 10

   def get_context_data(self, **kwargs):
       context = super(UsersWork, self).get_context_data(**kwargs)
       context['groups'] = Group.objects.all()
       return context


class UserDetailView(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    login_url = '/'
    permission_required = "auth.change_user"
    queryset = User.objects.using('default').all()
    context_object_name = 'user_detail'
    template_name = 'users/user_detail.html'

"""
    Work with MainCategory
"""


class MainCategoryWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'maincategory/mcwork.html'
    context_object_name = 'mc_list'
    paginate_by = 10
    model = MainCategory

    def get_context_data(self, **kwargs):
        context = super(MainCategoryWork, self).get_context_data(**kwargs)
        context['tab'] = True
        return context


class AjaxMainCategoryNew(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            name_url = self.slugify(request.GET['name'])
            new_mc = MainCategory.objects.save_new_category(self.request.GET['name'], self.slugify(request.GET['name']))
            return JsonResponse({"status": True, 'id': new_mc.id, 'name_url': name_url})

    def slugify(self, str):
        import re
        import unidecode
        string = re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())
        return re.sub(r"'", '', string)


class AjaxMainCategoryActive(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = MainCategory.objects.change_active_status(kwargs['pk'])
            return JsonResponse(data)


class MainCategoryDelete(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        MainCategory.objects.get(pk=kwargs['pk']).delete()
        return redirect('/adminnv/maincategory/')


"""
    Work with Name Product
"""


class NameProductWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'nameproduct/npwork.html'
    context_object_name = 'np_list'
    paginate_by = 5
    model = NameProduct

    def get_context_data(self, **kwargs):
        context = super(NameProductWork, self).get_context_data(**kwargs)
        context['tab'] = True
        return context


class AjaxNameProductNew(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            name_url = self.slugify(request.GET['name'])
            new_np = NameProduct.objects.save_new_nameproduct(request.GET['name'], name_url)

            return JsonResponse({"status": True, 'id':new_np.id, 'name_url': name_url})

    def slugify(self, strg):
        import re
        import unidecode
        string = re.sub(r'\s+', '-', unidecode.unidecode(strg).lower().strip())
        return re.sub(r"'", '', string)


class AjaxNameProductActive(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = NameProduct.objects.change_active_status(kwargs['pk'])

            return JsonResponse(data)


class NameProductDelete(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        NameProduct.objects.get(pk=kwargs['pk']).delete()
        redirect_url = '/adminnv/nameproduct/'
        return redirect(redirect_url)


"""----------------Work with Size Table---------------------------"""


class SizeTableWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'sizes/sizeswork.html'
    context_object_name = 'st_list'
    model = SizeTable

    def get_context_data(self, **kwargs):
        context = super(SizeTableWork, self).get_context_data(**kwargs)
        context['tab'] = True
        context['main_category_list'] = MainCategory.objects.get_active_categories()
        return context


class SizeTableAddNew(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    form_class = SizeTableForm
    template_name = 'sizes/sizeswork.html'
    succes_url = '/adminnv/sizetable/'

    def form_valid(self, form):
        instance = form.save()
        return super(SizeTableAddNew, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['data'] = self.request.POST

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SizeTableAddNew, self).get_context_data(**kwargs)
        context['tab'] = True
        context['main_category_list'] = MainCategory.objects.get_active_categories()
        return context

    def get_success_url(self):
        return self.succes_url


class SizeTableDelete(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        SizeTable.objects.get(pk=kwargs['pk']).delete()
        redirect_url = '/adminnv/sizetable/'
        return redirect(redirect_url)


class AjaxGetSizes(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = SizeTable.objects.get_size_data(kwargs['pk'])
            return JsonResponse(list(data), safe=False)


"""---------------Work with Brends -------------------------------"""


class BrendsWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'brends/brwork.html'
    context_object_name = 'br_list'
    model = Brends

    def get_context_data(self, **kwargs):
        context = super(BrendsWork, self).get_context_data(**kwargs)
        context['tab'] = True
        return context


class AjaxBrendNew(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            name_url = self.slugify(request.GET['name'])
            new_br = Brends.objects.save_new_brend(name=self.request.GET['name'], name_url=name_url)
            return JsonResponse({"status": True, 'id': new_br.id, 'name_url': name_url})

    def slugify(self, strg):
        import re
        import unidecode
        string = re.sub(r'\s+', '-', unidecode.unidecode(strg).lower().strip())
        return re.sub(r"'", '', string)


class AjaxBrendActive(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = Brends.objects.change_active_status(kwargs['pk'])
            return JsonResponse(data)


class BrendDelete(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        Brends.objects.get(pk=kwargs['pk']).delete()
        redirect_url = '/adminnv/brends/'
        return redirect(redirect_url)


"""----------------Work with seasons---------------------------------"""


class SeasonsWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'seasons/seasonswork.html'
    context_object_name = 'se_list'
    model = Seasons

    def get_context_data(self, **kwargs):
        context = super(SeasonsWork, self).get_context_data(**kwargs)
        context['tab'] = True
        return context


class AjaxSeasonNew(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            name_url = self.slugify(request.GET['name'])
            new_se = Seasons.objects.save_new_season(name=self.request.GET['name'], name_url=name_url)
            return JsonResponse({"status": True, 'id': new_se.id, 'name_url': name_url})

    def slugify(self, strg):
        import re
        import unidecode
        string = re.sub(r'\s+', '-', unidecode.unidecode(strg).lower().strip())
        return re.sub(r"'", '', string)


class AjaxSeasonActive(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = Seasons.objects.change_active_status(kwargs['pk'])
            return JsonResponse(data)


class SeasonDelete(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        Seasons.objects.get(pk=kwargs['pk']).delete()
        redirect_url = '/adminnv/seasons/'
        return redirect(redirect_url)


"""---------------Work with Products-------------------------------"""


class ProductsWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    queryset = Products.objects.get_list_products()
    template_name = 'products/productswork.html'
    context_object_name = 'products_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ProductsWork, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_products'] = True

        return context


class CreateNewProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = "auth.change_user"
    form_class = ProductsForm
    template_name = 'products/createnewproduct.html'
    succes_url = '/adminnv/products/'

#Add request in kwargs variable for checked height[] data in clean()  method FormModel ProductsForm
    def get_form_kwargs(self):
        """
            This method is what injects forms with their keyword
            arguments.
        """
        # grab the current set of form #kwargs
        kwargs = super(CreateNewProduct, self).get_form_kwargs()
        # Update the kwargs with the request
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateNewProduct, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_products'] = True
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.identifier = self.uuid_sentece()
        instance.dirname_img = self.uuid_sentece_user()
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '_' + instance.identifier + '_' + form.cleaned_data['articul']
        genbarcode = SBS(form.cleaned_data['pre_barcode'])
        instance.barcode = genbarcode.generate_barcode()
        instance.save()

        self.save_other_files(instance, form)
        return super(CreateNewProduct, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['data'] = self.request.POST
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_products'] = True

        return self.render_to_response(context)

    def get_success_url(self):
        return self.succes_url

    def slugify(self, strg):
        import re
        import unidecode
        string = re.sub(r'\s+', '-', unidecode.unidecode(strg).lower().strip())
        return re.sub(r"'", '', string)

    def uuid_sentece_user(self):
        import uuid
        return 'product_' + str(uuid.uuid4())[:10]

    def uuid_sentece(self):
        import uuid
        return str(uuid.uuid4())[:10]

    def save_other_files(self, instance, form):
        if not os.path.exists(settings.BASE_DIR + '/ '+ settings.TEST_MEDIA_IMAGES+instance.dirname_img) and self.request.FILES.getlist('other_img[]'):
            os.mkdir(settings.BASE_DIR + '/' + settings.TEST_MEDIA_IMAGES+instance.dirname_img, mode=0o777)
        # https://docs.djangoproject.com/ja/1.11/_modules/django/utils/datastructures/ - look for MultiValueDict(getlist)
        if self.request.FILES.getlist('img_product[]'):
            os.chmod(settings.BASE_DIR + '/' + settings.TEST_MEDIA_IMAGES+instance.dirname_img, 0o777)
            for ifile in self.request.FILES.getlist('img_product[]'):
                if ifile.size < settings.MAX_SIZE_UPLOAD and ifile.content_type in settings.CONTENT_TYPES_FILE:
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/images/' + instance.dirname_img,
                                           base_url='media/images/' + instance.dirname_img)
                    filename = fs.save(ifile.name, ifile)
                    i = Image(products=instance,
                              img_path=fs.url(filename))
                    i.save()
                else:
                    # messages.info(self.request, 'Three credits remain in your account.')
                    continue
        return True


class EditProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = "auth.change_user"
    model = Products
    form_class = ProductsFormEdit
    context_object_name = 'data_product_edit'
    template_name = 'products/editproduct.html'
    success_url = '/adminnv/products/'

    # Add request in kwargs variable for checked height[] data in clean()  method FormModel ProductsForm
    def get_form_kwargs(self):
        """
            This method is what injects forms with their keyword
            arguments.
        """
        # grab the current set of form #kwargs
        kwargs = super(EditProduct, self).get_form_kwargs()
        # Update the kwargs with the request
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EditProduct, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_products'] = True
        context['image_num'] = range(5)
        context['action'] = reverse('editproduct',
                                    kwargs={'pk': self.get_object().id})

        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '_' + instance.identifier + '_' + form.cleaned_data['articul']
        instance.is_new_date_end = date.today() + timedelta(days=settings.DNP) if instance.is_new else date.today()
        instance.save()

        return super(EditProduct, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['data'] = self.request.POST
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['action'] = reverse('editproduct', kwargs={'pk': self.get_object().id})
        context['tab_products'] = True

        return self.render_to_response(context)

    def slugify(self, strg):
        import re
        import unidecode
        string = re.sub(r'\s+', '-', unidecode.unidecode(strg).lower().strip())
        return re.sub(r"'", '', string)

    def uuid_sentece_user(self):
        import uuid
        return 'product_' + str(uuid.uuid4())[:10]

    def uuid_sentece(self):
        import uuid
        return str(uuid.uuid4())[:10]


class ViewProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = "auth.change_user"
    login_url = 'login'
    model = Products
    template_name = 'products/detailview.html'
    context_object_name = 'product_data'

    def get_context_data(self, **kwargs):
        context = super(ViewProduct, self).get_context_data(**kwargs)
        context['tab_products'] = True
        return context


class DeleteProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "auth.change_user"
    login_url = 'login'
    model = Products
    success_url = reverse_lazy('products')
    context_object_name = 'data_product_delete'
    template_name = 'products/deleteproduct.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteProduct, self).get_context_data(**kwargs)
        context['tab_products'] = True
        return context

    def delete(self, request, *args, **kwargs):
        return super(DeleteProduct, self).delete(self, request, *args, **kwargs)


class CheckIssetArticul(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
           product_result = Products.objects.check_isset_articul(kwargs['articul'])
           return JsonResponse({"status": product_result})


class CheckIssetPreBarcode(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
           product_result = Products.objects.check_isset_pre_barcode(kwargs['pre_barcode'])
        return JsonResponse({"status": product_result})


class CheckIssetModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            product_result = Modelss.objects.check_isset_modelss(kwargs['modelss'])
            return JsonResponse({"status": product_result})


class FoundArticul(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'products/detailview.html'

    def post(self, request):
        form = FoundArticuls(request.POST)
        if form.is_valid():
            articul = form.cleaned_data['articul']
            args = {'tab_products': True,
                    'product_data': Products.objects.found_articul(articul)}
            return render(request, self.template_name, args)
        else:
            args = {'tab_products': True,
                    'product_data': False}
            return render(request, self.template_name, args)


class FoundsModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'detailmodelss.html'

    def post(self, request):
        form = FoundModelss(request.POST)
        if form.is_valid():
            modelss = form.cleaned_data['modelss']
            args = {'tab_products': True,
                    'products': Products.objects.found_modelss(modelss)}
            return render(request, self.template_name, args)
        else:
            args = {'tab_products': True,
                    'products': False}
            return render(request, self.template_name, args)


class FilterProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'products/filterproducts.html'
    context_object_name = 'products_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(FilterProduct, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_products'] = True

        return context

    def get(self, request, *args, **kwargs):
        """
        If submit search form, add more options
        """
        form = FilterProducts(request.GET)
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

    def get_queryset(self):
        return Products.objects.filter_products(self.data)


class SaleViewProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'products/saleviewproduct.html'
    context_object_name = 'sale_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(SaleViewProduct, self).get_context_data(**kwargs)
        context['product_data'] = Products.objects.get_single_product(self.kwargs['pk'])
        context['tab_products'] = True

        return context

    def get(self, request, *args, **kwargs):
        """
        If submit search form, add more options
        """
        if request.GET.getlist('submit'):
            form = FilterSaleProduct(request.GET)
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
                context['data_form'] = form.cleaned_data
                context['form'] = form
                return render(request, self.template_name, context)
        else:
            self.data = dict()
            self.object_list = self.get_queryset()
            return render(request, self.template_name, self.get_context_data())

    def get_queryset(self):
        return ProductsSale.objects.get_list_data(self.kwargs['pk'], self.data)