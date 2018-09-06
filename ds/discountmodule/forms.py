from django import forms


class FilterDiscounts(forms.Form):
    description_f = forms.CharField(required=False)
    disco_value = forms.IntegerField(required=True, error_messages={'required': 'Введите скидку'})
    maincategory_id = forms.CharField(required=False)
    nameproduct_id = forms.CharField(required=False)
    brends = forms.CharField(required=False)
    season_id = forms.CharField(required=False)