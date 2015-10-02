# coding=utf-8

from django import forms

from recomendacao.choices import choices_mode


class FormText(forms.Form):
    text = forms.CharField(widget=forms.Textarea,)
    mode = forms.ChoiceField(choices=choices_mode())
    
    class Meta:
        fields = ['text', 'mode']
        localized_fields = '__all__'
