# coding=utf-8

from django import forms


class FormTexto(forms.Form):
    texto = forms.CharField(widget=forms.Textarea,)
    
    class Meta:
        fields = ['texto',]
        localized_fields = '__all__'
