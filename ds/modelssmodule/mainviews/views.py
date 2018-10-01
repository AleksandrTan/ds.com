import os
import shutil

from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse_lazy, reverse

from dsadminvn.mainviews.views import BaseAdminView
from dsstore.models import (MainCategory, NameProduct, Brends, Seasons, Products, Modelss,
                            ModelssForm, ProductsFormEdit, Image, )
from modelssmodule.mainhelpers.savedproducts import SavedProducts
from modelssmodule.forms import FoundModelss


class ModelssWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    queryset = Modelss.objects.get_list_products()
    template_name = 'modelssview.html'
    context_object_name = 'modelss_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ModelssWork, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_modelss'] = True

        return context


class CreateNewModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = "auth.change_user"
    form_class = ModelssForm
    template_name = 'createmodelss.html'
    succes_url = '/adminnv/products/modelss/'

#Add request in kwargs variable for checked height[] data in clean()  method FormModel ProductsForm
    def get_form_kwargs(self):
        """
            This method is what injects forms with their keyword
            arguments.
        """
        # grab the current set of form #kwargs
        kwargs = super(CreateNewModelss, self).get_form_kwargs()
        # Update the kwargs with the request
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateNewModelss, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['sizes_table'] = context['maincategorys'][0].sizetable_set.all()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_modelss'] = True
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.identifier = self.uuid_sentece()
        instance.dirname_img = self.uuid_sentece_user()
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '_' + instance.identifier + '_' + form.cleaned_data['name']
        instance.save()

        self.save_other_files(instance, form)
        if self.request.POST.getlist('product_data_lists'):
            result_products = SavedProducts(instance, self.request)
            result = result_products.saved_products()
            if not result:
                return super(CreateNewModelss, self).form_valid(form)
            else:
                context = self.get_context_data()
                context['erros_product'] = result
                return self.render_to_response(context)
        else:
            return super(CreateNewModelss, self).form_valid(form)

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
        return 'modelss_' + str(uuid.uuid4())[:10]

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
                    i = Image(modelss=instance,
                              img_path=fs.url(filename))
                    i.save()
                else:
                    # messages.info(self.request, 'Three credits remain in your account.')
                    continue
        return True


class EditModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
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
        kwargs = super(EditModelss, self).get_form_kwargs()
        # Update the kwargs with the request
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EditModelss, self).get_context_data(**kwargs)
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
            instance.main_photo_path = 'nophoto.png'
        if int(self.request.POST['is_del_other_photo']) == 1:
            self.delete_related_photo(instance, self.request.POST['list_del_other_photo'])
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '_' + instance.identifier + '_' + form.cleaned_data['articul']
        instance.save()
        self.save_other_files(instance, form)

        return super(EditModelss, self).form_valid(form)

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
        return 'modelss_' + str(uuid.uuid4())[:10]

    def uuid_sentece(self):
        import uuid
        return str(uuid.uuid4())[:10]

    def save_other_files(self, instance, form):
        if not os.path.exists(settings.BASE_DIR + '/' + settings.TEST_MEDIA_IMAGES+instance.dirname_img) and self.request.FILES.getlist('other_img[]'):
            os.mkdir(settings.BASE_DIR + '/' + settings.TEST_MEDIA_IMAGES+instance.dirname_img, mode=0o777)
        # https://docs.djangoproject.com/ja/1.11/_modules/django/utils/datastructures/ - look for MultiValueDict(getlist)
        if self.request.FILES.getlist('img_product[]'):
            os.chmod(settings.BASE_DIR + '/' + settings.TEST_MEDIA_IMAGES+instance.dirname_img, 0o777)
            for ifile in self.request.FILES.getlist('img_product[]'):
                if ifile.size < settings.MAX_SIZE_UPLOAD and ifile.content_type in settings.CONTENT_TYPES_FILE:
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/images/' + instance.dirname_img,
                                           base_url='media/images/' + instance.dirname_img)
                    filename = fs.save(ifile.name, ifile)
                    i = Image(modelss=instance,
                              img_path=fs.url(filename))
                    i.save()
                else:
                    # messages.info(self.request, 'Three credits remain in your account.')
                    continue
        return True

    # def saved_sizes_count(self, instance):
    #     # map(lambda x: x.save(),
    #     #     [SizeCount(products=instance, size=sizes[0], count_num=sizes[1]) for sizes in data_list])
    #     data_list = zip(self.request.POST.getlist('height[]'), self.request.POST.getlist('count_height[]'))
    #     edit_data = [SizeCount(products=instance, size=sizes[0], count_num=sizes[1]) for sizes in data_list]
    #     #update sizecount data(poducts_id set null in table field) inserted new data
    #     instance.sizecount.set(edit_data, clear=True, bulk=False)
    #     #delete old data
    #     SizeCount.objects.filter(products_id=None).delete()

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


class FoundsModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'detailmodelss.html'

    def post(self, request):
        form = FoundModelss(request.POST)
        if form.is_valid():
            modelss = form.cleaned_data['name']
            args = {'tab_modelss': True,
                    'modelss': Modelss.objects.found_modelss(modelss)}
            return render(request, self.template_name, args)
        else:
            args = {'tab_modelss': True,
                    'modelss': False}
            return render(request, self.template_name, args)


class DeleteModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "auth.change_user"
    login_url = 'login'
    model = Modelss
    success_url = reverse_lazy('modelss')
    context_object_name = 'data_modelss_delete'
    template_name = 'deletemodelss.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteModelss, self).get_context_data(**kwargs)
        context['tab_modelss'] = True
        return context

    def delete(self, request, *args, **kwargs):
        self.delete_images_dir()
        return super(DeleteModelss, self).delete(self, request, *args, **kwargs)

    def delete_images_dir(self):
        obj = self.get_object()
        path = settings.BASE_DIR + '/' + settings.TEST_MEDIA_IMAGES+obj.dirname_img
        #path = settings.MEDIA_ROOT + '\\images\\' + obj.dirname_img
        shutil.rmtree(path, ignore_errors=True)

    # def get_success_url(self):
    #     return self.request.POST['next_url']