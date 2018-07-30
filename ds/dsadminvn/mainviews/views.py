import os
import shutil

from django.conf import settings
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import QueryDict

from django.contrib.auth.models import User
from dsstore.models import (MainCategory, NameProduct, SizeTable,
                            SizeTableForm, Brends, Seasons, Products,
                            ProductsForm, ProductsFormEdit, Image, SizeCount)

from dsadminvn.forms import FoundArticuls, FilterProducts


class BaseAdminView(View):
    """
    Base view for admin views.
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    Look in Python3\Lib\site-packages\django\contrib\admin\views\decorators.py
            Python3\Lib\site-packages\django\contrib\auth\decorators.py
            Python3\Lib\site-packages\django\contrib\admindocs\views.py
    """
    @method_decorator(staff_member_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(BaseAdminView, self).dispatch(request, *args, **kwargs)

#Class MainView  - start page


class MainView(BaseAdminView, LoginRequiredMixin, TemplateView):
   template_name = 'index.html'
   login_url = 'login'

   # def get_context_data(self, **kwargs):
   #    content = super(MainView, self).get_context_data(**kwargs)
   #    content['count_new_sentences'] = Sentence.objects.filter(on_moderation=0).count()
   #    return content

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
        return JsonResponse({"status": True, 'id':new_mc.id, 'name_url':name_url})

    def slugify(swlf, str):
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
        redirect_url = '/adminnv/maincategory/'
        return redirect(redirect_url)

    def get_context_data(self, **kwargs):
        context = super(MainCategoryDelete, self).get_context_data(**kwargs)
        context['tab'] = True
        return context

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
            new_np =  NameProduct.objects.save_new_nameproduct(request.GET['name'], name_url)

        return JsonResponse({"status": True, 'id':new_np.id, 'name_url':name_url})

    def slugify(swlf, str):
        import re
        import unidecode
        return re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())


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

    def get_context_data(self, **kwargs):
        context = super(NameProductDelete, self).get_context_data(**kwargs)
        context['tab'] = True
        return context

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

    def get_context_data(self, **kwargs):
        context = super(NameProductDelete, self).get_context_data(**kwargs)
        context['tab'] = True
        return context


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
            new_br =  Brends.objects.save_new_brend(name=self.request.GET['name'], name_url=name_url)
        return JsonResponse({"status": True, 'id':new_br.id, 'name_url':name_url})

    def slugify(swlf, str):
        import re
        import unidecode
        return re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())


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

    def get_context_data(self, **kwargs):
        context = super(BrendDelete, self).get_context_data(**kwargs)
        context['tab'] = True
        return context

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
            new_se =  Seasons.objects.save_new_season(name=self.request.GET['name'], name_url=name_url)
        return JsonResponse({"status": True, 'id':new_se.id, 'name_url':name_url})

    def slugify(swlf, str):
        import re
        import unidecode
        return re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())


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

    def get_context_data(self, **kwargs):
        context = super(SeasonDelete, self).get_context_data(**kwargs)
        context['tab'] = True
        return context

"""---------------Work with Products-------------------------------"""


class ProductsWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    queryset = Products.objects.get_list_products()
    template_name = 'products/productswork.html'
    context_object_name = 'products_list'
    paginate_by = 5

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
        import dsadminvn.mainhelpers.SetBarcode as SB
        instance = form.save(commit=False)
        instance.identifier = self.uuid_sentece()
        instance.dirname_img = self.uuid_sentece_user()
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '-' + instance.identifier + '#' + form.cleaned_data['articul']
        genbarcode = SB.SetBarcode(form.cleaned_data['pre_barcode'])
        instance.barcode = genbarcode.generate_barcode()
        instance.save()

        self.save_oter_files(instance, form)
        self.saved_sizes_count(instance)
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

    def save_oter_files(self, instance, form):
        if not os.path.isdir(settings.TEST_MEDIA_IMAGES + instance.dirname_img) and self.request.FILES.getlist('other_img[]'):
            os.mkdir(settings.TEST_MEDIA_IMAGES + instance.dirname_img, mode=0o777)
        # https://docs.djangoproject.com/ja/1.11/_modules/django/utils/datastructures/ - look for MultiValueDict(getlist)
        if self.request.FILES.getlist('img_product[]'):
            for ifile in self.request.FILES.getlist('img_product[]'):
                if ifile.size < settings.MAX_SIZE_UPLOAD and ifile.content_type in settings.CONTENT_TYPES_FILE:
                    fs = FileSystemStorage(location=settings.TEST_MEDIA_IMAGES + instance.dirname_img,
                                           base_url=settings.TEST_MEDIA_IMAGES + instance.dirname_img)
                    filename = fs.save(ifile.name, ifile)
                    i = Image(products=instance,
                              img_path=fs.url(filename))
                    i.save()
                else:
                    # messages.info(self.request, 'Three credits remain in your account.')
                    continue
        return True

    def saved_sizes_count(self, instance):
        # map(lambda x: x.save(),
        #     [SizeCount(products=instance, size=sizes[0], count_num=sizes[1]) for sizes in data_list])
        data_list = zip(self.request.POST.getlist('height[]'), self.request.POST.getlist('count_height[]'))
        d = [SizeCount(products=instance, size=sizes[0], count_num=sizes[1]) for sizes in data_list]
        for sizes in d:
            sizes.save()


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

    # def get_success_url(self):
    #     return self.request.build_absolute_uri()

    def form_valid(self, form):
        instance = form.save(commit=False)
        #delete main file photo
        if int(self.request.POST['is_del_mainphoto']) == 0:
            instance.main_photo_path.delete()
            instance.main_photo_path = 'nophoto.png'
        if int(self.request.POST['is_del_other_photo']) == 1:
            self.delete_related_photo(instance, self.request.POST['list_del_other_photo'])
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '-' + instance.identifier + '#' + form.cleaned_data['articul']
        instance.save()
        self.save_oter_files(instance, form)
        self.saved_sizes_count(instance)

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

    def save_oter_files(self, instance, form):
        if not os.path.isdir(settings.TEST_MEDIA_IMAGES + instance.dirname_img) and self.request.FILES.getlist('other_img[]'):
            os.mkdir(settings.TEST_MEDIA_IMAGES + instance.dirname_img, mode=0o777)
        # https://docs.djangoproject.com/ja/1.11/_modules/django/utils/datastructures/ - look for MultiValueDict(getlist)
        if self.request.FILES.getlist('img_product[]'):
            for ifile in self.request.FILES.getlist('img_product[]'):
                if ifile.size < settings.MAX_SIZE_UPLOAD and ifile.content_type in settings.CONTENT_TYPES_FILE:
                    fs = FileSystemStorage(location=settings.TEST_MEDIA_IMAGES + instance.dirname_img,
                                           base_url=settings.TEST_MEDIA_IMAGES + instance.dirname_img)
                    filename = fs.save(ifile.name, ifile)
                    i = Image(products=instance,
                              img_path=fs.url(filename))
                    i.save()
                else:
                    # messages.info(self.request, 'Three credits remain in your account.')
                    continue
        return True

    def saved_sizes_count(self, instance):
        # map(lambda x: x.save(),
        #     [SizeCount(products=instance, size=sizes[0], count_num=sizes[1]) for sizes in data_list])
        data_list = zip(self.request.POST.getlist('height[]'), self.request.POST.getlist('count_height[]'))
        edit_data = [SizeCount(products=instance, size=sizes[0], count_num=sizes[1]) for sizes in data_list]
        #update sizecount data(poducts_id set null in table field) inserted new data
        instance.sizecount.set(edit_data, clear=True, bulk=False)
        #delete old data
        SizeCount.objects.filter(products_id=None).delete()

    def delete_related_photo(self, instance, file_list):
        import json
        data = json.loads(file_list)
        for imaje in data:
            img = Image.objects.filter(id=imaje).get()
            try:
                os.remove(settings.BASE_DIR + '/' + img.img_path)
                img.delete()
            except OSError:
               pass


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
        self.delete_images_dir()
        return super(DeleteProduct, self).delete(self, request, *args, **kwargs)

    def delete_images_dir(self):
        obj = self.get_object()
        path = settings.MEDIA_ROOT + '\\images\\' + obj.dirname_img
        shutil.rmtree(path, ignore_errors=True)

    # def get_success_url(self):
    #     return self.request.get_full_path()


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


class FoundArticul(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'products/detailview.html'

    def post(self, request):
        form = FoundArticuls(request.POST)
        if form.is_valid():
            articul = form.cleaned_data['articul']
            args = {'tab_products':True,
                    'product_data':Products.objects.found_articul(articul)}
            return render(request, self.template_name, args)
        else:
            args = {'tab_products': True,
                    'product_data': False}
            return render(request, self.template_name, args)


class FilterProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'products/filterproducts.html'
    context_object_name = 'products_list'
    paginate_by = 5

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
            self.object_list = self.get_queryset(form.cleaned_data)
            context = self.get_context_data(object_list=self.object_list)
            context['data_form'] = form.cleaned_data
            copy_get = QueryDict(request.GET.copy().urlencode(), mutable=True)
            copy_get['submit'] = 0
            context['request_get'] = copy_get.urlencode()
            return render(request, self.template_name, context)
        else:
            self.object_list = self.get_queryset(form.cleaned_data)
            context = self.get_context_data(object_list=self.object_list)
            context['form'] = form
            return render(request, self.template_name, context)

    def get_queryset(self, data):
        return Products.objects.filter_products(data)
