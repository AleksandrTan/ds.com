from django import forms

class FoundArticuls(forms.Form):
    articul  = forms.CharField(max_length=6, label='articul')

class FilterProduct(forms.Form):
    pass