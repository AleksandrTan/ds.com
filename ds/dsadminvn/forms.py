from django import forms


class FoundArticuls(forms.Form):
    articul = forms.CharField(max_length=6, label='articul')


class FoundModelss(forms.Form):
    modelss = forms.CharField(max_length=50, label='modelss')


class FilterProducts(forms.Form):
    maincategory_id = forms.CharField(required=False)
    nameproduct_id = forms.CharField(required=False)
    brends = forms.CharField(required=False)
    season_id = forms.CharField(required=False)
    is_belarus = forms.BooleanField(required=False)
    is_active =forms.BooleanField(required=False)
    is_new = forms.BooleanField(required=False)


class FilterSaleProduct(forms.Form):
    date_with = forms.DateField(required=False)
    date_by = forms.DateField(required=False)
