from django.forms import formset_factory
from django import forms


class BarcodeSellProduct(forms.Form):
    products = forms.CharField(required=False, widget=forms.HiddenInput)
    lost_num = forms.CharField(required=False)


BarcodeFormSet = formset_factory(BarcodeSellProduct, extra=2, max_num=100)