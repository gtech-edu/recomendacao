# coding=utf-8

from django import forms


class FormText(forms.Form):
    text = forms.CharField(widget=forms.Textarea,)
    
    class Meta:
        fields = ['text',]
        localized_fields = '__all__'
