# coding=utf-8

from django import forms

from recomendacao.choices import choices_mode
from recomendacao.defaults import CACHE_RELOAD


class FormText(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    mode = forms.ChoiceField(choices=choices_mode(), initial='default', required=False)
    images = forms.BooleanField(initial=False, required=False)
    cache_reload = forms.IntegerField(initial=CACHE_RELOAD, required=False)

    class Meta:
        fields = ['text', 'mode', 'images', 'cache_reload']
        localized_fields = '__all__'
