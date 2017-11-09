from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from django.contrib.auth.models import User

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
   queryset = User.objects.using('default').all()
   context_object_name = 'users_list' #or for custom paginate page_obj in template
   paginate_by = 10