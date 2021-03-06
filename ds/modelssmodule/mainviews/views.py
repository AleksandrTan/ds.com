import os
import shutil
from datetime import timedelta, date

from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import QueryDict

from dsadminvn.mainviews.views import BaseAdminView
from dsstore.models import (MainCategory, NameProduct, Brends, Seasons, Modelss,
                            ModelssForm, ModelssFormEdit, Image)
from modelssmodule.mainhelpers.savedproducts import SavedProducts
from modelssmodule.mainhelpers.addproducts import AddProducts
from modelssmodule.forms import FoundModelss, FilterModel


class ModelssWork(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    queryset = Modelss.objects.get_list_products()
    template_name = 'modelssview.html'
    context_object_name = 'modelss_list'
    paginate_by = 20

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
    succes_url = '/adminnv/products/modelss/viewmodelss/{0}/'

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
        instance.is_new_date_end = date.today() + timedelta(days=settings.DNP) if instance.is_new else date.today()
        instance.save()

        self.save_other_files(instance, form)
        if self.request.POST.getlist('product_data_lists')[0] != '':
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
        return self.succes_url.format(self.object.id)

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
        if not os.path.exists(settings.BASE_DIR + '/ ' + settings.TEST_MEDIA_IMAGES+instance.dirname_img) and self.request.FILES.getlist('other_img[]'):
            os.mkdir(settings.BASE_DIR + '/' + settings.TEST_MEDIA_IMAGES+instance.dirname_img, mode=0o777)
        # https://docs.djangoproject.com/ja/1.11/_modules/django/utils/datastructures/ - look for MultiValueDict(getlist)
        if self.request.FILES.getlist('img_product[]'):
            os.chmod(settings.BASE_DIR + '/' + settings.TEST_MEDIA_IMAGES+instance.dirname_img, 0o777)
            for ifile in self.request.FILES.getlist('img_product[]'):
                if ifile.size < settings.MAX_SIZE_UPLOAD and ifile.content_type in settings.CONTENT_TYPES_FILE:
                    # fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/images/' + instance.dirname_img,
                    #                        base_url='media/images/' + instance.dirname_img)
                    # filename = fs.save(ifile.name,ifile)
                    i = Image(modelss=instance,
                              img_path=ifile)
                    i.save()
                else:
                    # messages.info(self.request, 'Three credits remain in your account.')
                    continue
        return True


class EditModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = "auth.change_user"
    model = Modelss
    form_class = ModelssFormEdit
    context_object_name = 'data_modelss_edit'
    template_name = 'editmodelss.html'
    success_url = '/adminnv/products/modelss/viewmodelss/{0}/'

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
        context['tab_modelss'] = True
        context['image_num'] = range(5)
        context['action'] = reverse('editmodelss',
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
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '_' + instance.identifier + '_' + form.cleaned_data['name']
        instance.is_new_date_end = date.today() + timedelta(days=settings.DNP) if instance.is_new else date.today()
        instance.save()
        #send signal for update products in modelss
        from modelssmodule.signals.signal import model_update
        model_update.send(sender=Modelss, instance=instance)

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
        context['tab_modelss'] = True

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
                    # fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/images/' + instance.dirname_img,
                    #                        base_url='media/images/' + instance.dirname_img)
                    # filename = fs.save(ifile.name,ifile)
                    i = Image(modelss=instance,
                              img_path=ifile)
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
                img.delete()
                #os.remove(settings.BASE_DIR + '/' + img.img_path)
            except OSError:
               pass

    def get_success_url(self):
        return self.success_url.format(self.get_object().id)


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


class ViewModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = "auth.change_user"
    login_url = 'login'
    model = Modelss
    template_name = 'detailmodelss.html'
    context_object_name = 'modelss'

    def get_context_data(self, **kwargs):
        context = super(ViewModelss, self).get_context_data(**kwargs)
        context['tab_modelss'] = True
        return context


class FilterModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.change_user"
    login_url = 'login'
    template_name = 'filtermodelss.html'
    context_object_name = 'modelss_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(FilterModelss, self).get_context_data(**kwargs)
        context['maincategorys'] = MainCategory.objects.get_active_categories()
        context['nameproducts'] = NameProduct.objects.get_active_products()
        context['brends'] = Brends.objects.get_active_brends()
        context['seasons'] = Seasons.objects.get_active_seasons()
        context['tab_modelss'] = True

        return context

    def get(self, request, *args, **kwargs):
        """
        If submit search form, add more options
        """
        form = FilterModel(request.GET)
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
        return Modelss.objects.filter_modelss(self.data)


class AddProductModelss(BaseAdminView, LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'login'
    permission_required = "auth.change_user"
    template_name = 'addproductmodelss.html'
    success_url = '/adminnv/products/modelss/viewmodelss/{0}/'

    def get(self, request, **kwargs):
        args = {'tab_modelss': True,
                'modelss': Modelss.objects.get_modelss(kwargs['pk']),
                'action': reverse('addproductsmodelss', kwargs={'pk': kwargs['pk']})
                }
        if args['modelss']:
            args['isset_sizes'] = args['modelss'].products_set.values_list('size', flat=True)
        return render(request, self.template_name, args)

    def post(self, request, pk):
        instance = Modelss.objects.get_modelss(pk)
        if self.request.POST.getlist('product_data_lists')[0] != '':
            result_products = AddProducts(instance, self.request.POST.getlist('product_data_lists')[0])
            result = result_products.saved_products()
            if not result:
                return redirect(self.success_url.format(pk))
            else:
                args = {'tab_modelss': True,
                        'modelss': Modelss.objects.get_modelss(pk),
                        'action': reverse('addproductsmodelss',
                                          kwargs={'pk': pk}),
                        'hh': result
                        }
                return render(request, self.template_name, args)
        else:
            return redirect(self.success_url.format(pk))