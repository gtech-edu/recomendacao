# coding=utf-8

from rest_framework import serializers

from recomendacao.choices import choices_mode


class SerializerText(serializers.Serializer):
    text = serializers.CharField()
    mode = serializers.ChoiceField(choices=choices_mode(), required=False)
    
    class Meta:
        fields = ['text', 'mode']
        localized_fields = '__all__'
