from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.models import User
from dsstore.models import MainCategory

#Class MainView  - start page


class MainView(LoginRequiredMixin, TemplateView):

   template_name = 'index.html'

   # def get_context_data(self, **kwargs):
   #    content = super(MainView, self).get_context_data(**kwargs)
   #    content['count_new_sentences'] = Sentence.objects.filter(on_moderation=0).count()
   #    return content

"""
    Work with users site
"""

#Class UsersWork  - All users page

class UsersWork(LoginRequiredMixin, PermissionRequiredMixin, ListView):

   permission_required = "auth.change_user"
   template_name = 'users/users.html'
   login_url = '/'
   queryset = User.objects.all()
   context_object_name = 'users_list' #or for custom paginate page_obj in template
   paginate_by = 10


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    login_url = '/'
    permission_required = "auth.change_user"
    queryset = User.objects.using('default').all()
    context_object_name = 'user_detail'
    template_name = 'users/user_detail.html'


"""
    Work with Msn (MainCategory, Size, NameProduct)
"""

class MsnWork(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    data_db = {'maincategory':MainCategory}
    data_slug = {'maincategory': 'Категории'}
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