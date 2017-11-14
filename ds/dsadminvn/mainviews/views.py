from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from dsstore.models import MainCategory, NameProduct


class BaseAdminView(View):
    """
    Base view for admin views.
    """
    @method_decorator(staff_member_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(BaseAdminView, self).dispatch(request, *args, **kwargs)

#Class MainView  - start page


class MainView(BaseAdminView, LoginRequiredMixin, TemplateView):
   template_name = 'index.html'

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
   login_url = '/'
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
    Work with Msn (MainCategory, NameProduct)
"""

class MsnWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    data_db = {'maincategory':MainCategory,'nameproducts':NameProduct}
    data_slug = {'maincategory': 'Категории', 'nameproducts':'Название товара'}
    permission_required = "auth.change_user"
    login_url = '/'
    template_name = 'msn/msnwork.html'
    context_object_name = 'msn_list'
    paginate_by = 10

    def get_queryset(self):
        return self.data_db[self.kwargs['type_slug']].objects.all()

    def get_context_data(self, **kwargs):
        context = super(MsnWork, self).get_context_data(**kwargs)
        context['tab'] = True
        context['slug'] = self.data_slug[self.kwargs['type_slug']]
        context['key_slug'] = self.kwargs['type_slug']
        return context