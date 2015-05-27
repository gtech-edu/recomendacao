# coding=utf-8

from rest_framework import serializers


class SerializerTexto(serializers.Serializer):
    texto = serializers.CharField()
    
    class Meta:
        fields = ['texto',]
        localized_fields = '__all__'
