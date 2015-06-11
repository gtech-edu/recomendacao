# coding=utf-8

from rest_framework import serializers


class SerializerText(serializers.Serializer):
    text = serializers.CharField()
    
    class Meta:
        fields = ['text',]
        localized_fields = '__all__'
