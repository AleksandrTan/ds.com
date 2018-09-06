from django import forms


class FilterDiscounts(forms.Form):
    description_f = forms.CharField(required=False)
    disco_value = forms.IntegerField(required=True, error_messages={'required': 'Введите скидку'})
    maincategory_id = forms.CharField(required=False)
    nameproduct_id = forms.CharField(required=False)
    brends = forms.CharField(required=False)
    season_id = forms.CharField(required=False)


class ArticulDiscounts(forms.Form):
    description_a = forms.CharField(required=False)
    art_disco = forms.IntegerField(required=True, error_messages={'required': 'Введите скидку'})
    articul = forms.CharField(required=True, error_messages={'required': 'Введите артикул'})


class ModelDiscounts(forms.Form):
    description_m = forms.CharField(required=False)
    mod_disco = forms.IntegerField(required=True, error_messages={'required': 'Введите скидку'})
    modelss = forms.CharField(required=True, error_messages={'required': 'Введите артикул'})