import os
import shutil
from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from dsstore.models import (MainCategory, NameProduct, SizeTable, SizeTableForm, Brends, Seasons, Products, ProductsForm)

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
        return re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())

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
            data = SizeTable.objects.get_category_data(kwargs['pk'])
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

    def get_context_data(self, **kwargs):
        context = super(ProductsWork, self).get_context_data(**kwargs)
        context['tab_products'] = True
        return context

class ShowFormProductView(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'products/createnewproduct.html'

    def get_context_data(self, **kwargs):
        context = super(ShowFormProductView, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_products'] = True

        return context

class CreateNewProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    form_class = ProductsForm
    template_name = 'products/createnewproduct.html'
    succes_url = '/adminnv/products/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.stop_time = datetime.now() + timedelta(days=30)
        instance.type_img_s = self.type_img_s[form.cleaned_data['type_id']]
        instance.identifier = self.uuid_sentece()
        instance.dirname_img = self.uuid_sentece_user()
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '#' + instance.identifier
        instance.save()
        self.save_oter_files(instance, form)

        return super(CreateNewProduct, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['data'] = self.request.POST

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(CreateNewProduct, self).get_context_data(**kwargs)

        return context

    def get_success_url(self):
        return self.succes_url

    def slugify(swlf, str):
        import re
        import unidecode
        return re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())

    def uuid_sentece_user(self):
        import uuid
        return 'user_' + str(uuid.uuid4())[:10]

    def uuid_sentece(self):
        import uuid
        return str(uuid.uuid4())[:10]

    def save_oter_files(self, instance, form):
        if not os.path.isdir(settings.TEST_MEDIA_IMAGES + instance.dirname_img) and self.request.FILES.getlist(
                'other_img[]'):
            os.mkdir(settings.TEST_MEDIA_IMAGES + instance.dirname_img, mode=0o777)
        # https://docs.djangoproject.com/ja/1.11/_modules/django/utils/datastructures/ - look for MultiValueDict(getlist)
        if self.request.FILES.getlist('other_img[]'):
            for ifile in self.request.FILES.getlist('other_img[]'):
                if ifile.size < settings.MAX_SIZE_UPLOAD and ifile.content_type in settings.CONTENT_TYPES_FILE:
                    fs = FileSystemStorage(location=settings.TEST_MEDIA_IMAGES + instance.dirname_img,
                                           base_url=settings.TEST_MEDIA_IMAGES + instance.dirname_img)
                    filename = fs.save(ifile.name, ifile)
                    i = Image(sentence=instance,
                              img_path=fs.url(filename))
                    i.save()
                else:
                    # messages.info(self.request, 'Three credits remain in your account.')
                    continue
        return True

class EditProduct(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    pass