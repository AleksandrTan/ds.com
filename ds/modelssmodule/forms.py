from django import forms


class FoundModelss(forms.Form):
    name = forms.CharField(max_length=50, label='modelss')
