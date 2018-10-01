from django import forms


class FoundModelss(forms.Form):
    name = forms.CharField(max_length=50, label='modelss')


class FilterModel(forms.Form):
    maincategory_id = forms.CharField(required=False)
    nameproduct_id = forms.CharField(required=False)
    brends = forms.CharField(required=False)
    season_id = forms.CharField(required=False)
    is_belarus = forms.BooleanField(required=False)
    is_active =forms.BooleanField(required=False)
    is_new = forms.BooleanField(required=False)
