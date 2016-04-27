# coding=utf-8

from rest_framework import serializers

from recomendacao.choices import choices_mode
from recomendacao.defaults import CACHE_RELOAD


class SerializerText(serializers.Serializer):
    text = serializers.CharField()
    mode = serializers.ChoiceField(choices=choices_mode(), default='default', required=False)
    images = serializers.BooleanField(default=False, required=False)
    cache_reload = serializers.IntegerField(default=CACHE_RELOAD, required=False)

    class Meta:
        fields = ['text', 'mode', 'images', 'cache_reload']
        localized_fields = '__all__'
