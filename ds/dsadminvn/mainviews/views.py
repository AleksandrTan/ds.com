from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from dsstore.models import MainCategory, NameProduct


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

#Class UsersWork  - All users page

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

#Class MainCategoryWork  - All categories page

class MainCategoryWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'maincategory/mcwork.html'
    context_object_name = 'mc_list'
    paginate_by = 10

    def get_queryset(self):
        return MainCategory.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MainCategoryWork, self).get_context_data(**kwargs)
        context['tab'] = True
        return context

class AjaxMainCategoryNew(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            name_url = self.slugify(request.GET['name'])
            new_mc =  MainCategory(
                name=self.request.GET['name'],
                name_url=name_url,
                is_active=False
            )
            new_mc.save()

        return JsonResponse({"status": True, 'id':new_mc.id, 'name_url':name_url})

    def slugify(swlf, str):
        import re
        import unidecode
        return re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())

class AjaxMainCategoryActive(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            mc = MainCategory.objects.get(pk=kwargs['pk'])
            if mc.is_active:
                mc.is_active = False
                data = {"status":False}
            else:
                mc.is_active = True
                data = {"status": True}
        mc.save()
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

#Class NameProductWork  - All products page

class NameProductWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'nameproduct/npwork.html'
    context_object_name = 'np_list'
    paginate_by = 5

    def get_queryset(self):
        return NameProduct.objects.all()

    def get_context_data(self, **kwargs):
        context = super(NameProductWork, self).get_context_data(**kwargs)
        context['tab'] = True
        return context

class AjaxNameProductNew(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            name_url = self.slugify(request.GET['name'])
            new_np =  NameProduct(
                name=self.request.GET['name'],
                name_url=name_url,
                is_active=False
            )
            new_np.save()

        return JsonResponse({"status": True, 'id':new_np.id, 'name_url':name_url})

    def slugify(swlf, str):
        import re
        import unidecode
        return re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())


class AjaxNameProductActive(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            np = NameProduct.objects.get(pk=kwargs['pk'])
            if np.is_active:
                np.is_active = False
                data = {"status":False}
            else:
                np.is_active = True
                data = {"status": True}
        np.save()
        return JsonResponse(data)


class NameProductDelete(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = "auth.change_user"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        NameProduct.objects.get(pk=kwargs['pk']).delete()
        redirect_url = '/adminnv/maincategory/'
        return redirect(redirect_url)

    def get_context_data(self, **kwargs):
        context = super(NameProductDelete, self).get_context_data(**kwargs)
        context['tab'] = True
        return context