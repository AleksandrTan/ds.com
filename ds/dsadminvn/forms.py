from django import forms

class FoundArticuls(forms.Form):
    articul  = forms.CharField(max_length=6, label='articul')

class FilterProducts(forms.Form):
    maincategory = forms.CharField(required=False)
    nameproduct = forms.CharField(required=False)
    brends = forms.CharField(required=False)
    season_id = forms.CharField(required=False)
    is_belarus = forms.BooleanField(required=False)
    is_active =forms.BooleanField(required=False)
    is_new = forms.BooleanField(required=False)
